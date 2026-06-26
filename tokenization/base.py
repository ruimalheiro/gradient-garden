from abc import ABC, abstractmethod


class PromptBuilder:
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

    def add_message(self, role, content, *, supervise=False, final_assistant=False):
        if role == 'assistant':
            prefix = 'Assistant: '
            self.push(self.encode(prefix), supervise=False)
            if final_assistant:
                text = content + self.eos_token
            else:
                text = content + '\n'
            self.push(self.encode(text), supervise=supervise)
        else:
            prefix = f'{role.capitalize()}: {content}\n'
            self.push(self.encode(prefix), supervise=False)

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
        self.tokens.insert(0, self.bos_id)
        if not self.no_labels:
            self.labels.insert(0, self.ignore_index)

        if self.no_labels:
            return self.tokens

        if len(self.tokens) != len(self.labels):
            raise ValueError(
                f'Tokens and labels length do not match: {len(self.tokens)} vs {len(self.labels)}'
            )

        # Shift labels for next‑token prediction
        shifted_labels = self.labels[1:] + [self.ignore_index]
        return self.tokens, shifted_labels

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

        prefix = 'Assistant: '
        builder.push(builder.encode(prefix))
        return builder.build()

    def encode_instruct_chat(self, *, conversation, ignore_index: int):
        builder = PromptBuilder(self, ignore_index=ignore_index)

        has_system = any(msg['role'] == 'system' for msg in conversation)
        if not has_system:
            builder.add_message('system', self.system_prompt)

        for idx, interaction in enumerate(conversation):
            role = interaction['role']
            content = interaction['content']
            is_assistant = (role == 'assistant')
            is_last_message = (idx == len(conversation) - 1)
            builder.add_message(
                role,
                content,
                supervise=is_assistant,
                final_assistant=(is_assistant and is_last_message)
            )
        return builder.build()

    def encode_instruct_chat_dpo(self, *, conversation, chosen: str, rejected: str, ignore_index: int):
        prefix_builder = PromptBuilder(self, ignore_index=ignore_index)

        for interaction in conversation:
            prefix_builder.add_message(interaction['role'], interaction['content'], supervise=False)

        prefix_builder.push(prefix_builder.encode('Assistant:'), supervise=False)

        def build_answer(answer):
            builder = prefix_builder.clone()
            ans_tokens = builder.encode(answer + self.eos_token)
            builder.push(ans_tokens, supervise=True)
            return builder.build()

        prompt_ids, _ = prefix_builder.build()
        chosen_ids, chosen_labels = build_answer(chosen)
        rejected_ids, rejected_labels = build_answer(rejected)

        return prompt_ids, chosen_ids, chosen_labels, rejected_ids, rejected_labels
