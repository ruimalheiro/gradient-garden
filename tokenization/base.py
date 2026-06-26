from abc import ABC, abstractmethod


class PromptBuilder:
    ROLE_NAMES = {
        'system': 'System',
        'user': 'User',
        'assistant': 'Assistant',
    }

    def __init__(self, tokenizer, *, ignore_index=None, no_labels=False):
        self.tokenizer = tokenizer
        if no_labels is False and ignore_index is None:
            raise ValueError('ignore_index cannot be None when building labels')
        self.ignore_index = ignore_index
        self.no_labels = no_labels
        self.system_prompt = tokenizer.system_prompt
        self.eos_token = tokenizer.eos_token
        self.bos_id = tokenizer.bos_id
        self.tokens = []
        self.labels = []

    def encode(self, text):
        return self.tokenizer.encode(text)

    def push(self, tok_ids, supervise=False):
        self.tokens.extend(tok_ids)
        if self.no_labels:
            return
        if supervise:
            self.labels.extend(tok_ids)
        else:
            self.labels.extend([self.ignore_index] * len(tok_ids))

    def role_prefix(self, role: str) -> str:
        if role not in self.ROLE_NAMES:
            raise ValueError(f'Unknown role: {role}')
        return f'{self.ROLE_NAMES[role]}: '

    def add_message(self, role, content, *, supervise=False, final_assistant=False):
        prefix = self.role_prefix(role)
        self.push(self.encode(prefix), supervise=False)

        if role == 'assistant':
            text = content + (self.eos_token if final_assistant else '\n')
            self.push(self.encode(text), supervise=supervise)
        else:
            self.push(self.encode(content + '\n'), supervise=False)

    def add_assistant_prefix(self):
        self.push(self.encode(self.role_prefix('assistant')), supervise=False)

    def clone(self):
        other = PromptBuilder(
            self.tokenizer,
            ignore_index=self.ignore_index,
            no_labels=self.no_labels
        )
        other.tokens = list(self.tokens)
        other.labels = list(self.labels)
        return other

    def build(self):
        tokens = [self.bos_id] + self.tokens

        if self.no_labels:
            return tokens

        labels = [self.ignore_index] + self.labels

        if len(tokens) != len(labels):
            raise ValueError(
                f'Tokens and labels length do not match: {len(tokens)} vs {len(labels)}'
            )

        # Shift labels for next‑token prediction
        shifted_labels = labels[1:] + [self.ignore_index]
        return tokens, shifted_labels

class BaseTokenizer(ABC):
    @abstractmethod
    def encode(self, text, *, bos=False, eos=False, allowed_special=set(), disallowed_special=()):
        ...

    @abstractmethod
    def decode(self, ids):
        ...

    def encode_instruct_inference(self, text: str, system_msg: bool = True):
        builder = PromptBuilder(self, no_labels=True)

        if system_msg:
            builder.add_message('system', self.system_prompt)

        builder.add_message('user', text)
        builder.add_assistant_prefix()

        return builder.build()

    def encode_instruct_chat(
        self,
        *,
        conversation,
        ignore_index: int,
        max_seq_len: int | None = None,
        trim_to_context: bool = False
    ):
        if not conversation or conversation[-1]['role'] != 'assistant':
            raise ValueError('Instruct conversation must end with an assistant message.')

        builder = PromptBuilder(self, ignore_index=ignore_index)

        has_system = any(msg['role'] == 'system' for msg in conversation)
        if not has_system:
            builder.add_message('system', self.system_prompt)

        for idx, interaction in enumerate(conversation):
            role = interaction['role']
            content = interaction['content']

            is_assistant = role == 'assistant'
            is_last_message = idx == len(conversation) - 1
            is_final_assistant = is_assistant and is_last_message

            builder.add_message(
                role,
                content,
                supervise=is_final_assistant,
                final_assistant=is_final_assistant
            )

        return builder.build()

    def encode_instruct_chat_dpo(
        self,
        *,
        conversation,
        chosen: str,
        rejected: str,
        ignore_index: int,
        max_seq_len: int | None = None,
        trim_to_context: bool = False
    ):
        prefix_builder = PromptBuilder(self, ignore_index=ignore_index)

        has_system = any(msg['role'] == 'system' for msg in conversation)
        if not has_system:
            prefix_builder.add_message('system', self.system_prompt)

        for interaction in conversation:
            prefix_builder.add_message(
                interaction['role'],
                interaction['content'],
                supervise=False,
            )

        prefix_builder.add_assistant_prefix()

        def build_answer(answer):
            builder = prefix_builder.clone()
            builder.push(builder.encode(answer + self.eos_token), supervise=True)
            return builder.build()

        prompt_ids, _ = prefix_builder.build()
        chosen_ids, chosen_labels = build_answer(chosen)
        rejected_ids, rejected_labels = build_answer(rejected)

        return prompt_ids, chosen_ids, chosen_labels, rejected_ids, rejected_labels
