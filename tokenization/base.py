from abc import ABC, abstractmethod


class PromptBuilder:
    def __init__(self, tokenizer, *, ignore_index=None, no_labels=False):
        self.tokenizer = tokenizer
        if no_labels is False and ignore_index is None:
            raise ValueError('ignore_index cannot be None when building labels')
        self.ignore_index = ignore_index
        self.no_labels = no_labels
        self.system_prompt = tokenizer.system_prompt
        self.bot = tokenizer.bos_id
        self.sh = tokenizer.sh_id
        self.eh = tokenizer.eh_id
        self.eot = tokenizer.eot_id
        self.eos = tokenizer.eos_id
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

    def add_header(self, system_msg=True):
        self.push([self.bot], supervise=False)
        if system_msg:
            self.add_role_prefix('system')
            self.push(self.encode(self.system_prompt), supervise=False)
            self.push([self.eot], supervise=False)

    def add_role_prefix(self, role):
        self.push([self.sh], supervise=False)
        self.push(self.encode(role), supervise=False)
        self.push([self.eh], supervise=False)
        self.push(self.encode('\n'), supervise=False)

    def add_message(self, role, text, *, supervise=False, final_assistant=False):
        self.add_role_prefix(role)
        self.push(self.encode(text), supervise=supervise)
        if final_assistant:
            self.push([self.eos], supervise=supervise)
        else:
            self.push([self.eot], supervise=supervise and role == 'assistant')

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
        if self.no_labels:
            return self.tokens

        if len(self.tokens) != len(self.labels):
            raise ValueError(
                f'Tokens and labels length do not match: {len(self.tokens)} vs {len(self.labels)}'
            )

        shifted_labels = self.labels[1:] + [self.ignore_index]

        return self.tokens, shifted_labels

class BaseTokenizer(ABC):

    @abstractmethod
    def encode(self, text, *, bos=False, eos=False, allowed_special=set(), disallowed_special=()):
        ...

    @abstractmethod
    def decode(self, ids):
        ...

    def encode_instruct_inference(
        self,
        text: str,
        system_msg: bool = True
    ):
        builder = PromptBuilder(self, no_labels=True)
        builder.add_header(system_msg=system_msg)
        builder.add_message('user', text, supervise=False)
        builder.add_role_prefix('assistant')
        return builder.build()

    def encode_instruct_chat(
        self,
        *,
        conversation: object,
        ignore_index: int
    ):
        builder = PromptBuilder(self, ignore_index=ignore_index)
        builder.add_header(system_msg=True)

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

    def encode_instruct_chat_dpo(
        self,
        *,
        conversation: object,
        chosen: str,
        rejected: str,
        ignore_index: int
    ):
        prefix = PromptBuilder(self, ignore_index=ignore_index)
        prefix.add_header(system_msg=True)

        for interaction in conversation:
            role = interaction['role']
            content = interaction['content']

            prefix.add_message(
                role,
                content,
                supervise=False,
                final_assistant=False
            )

        prefix.add_role_prefix('assistant')

        def build_answer(answer):
            builder = prefix.clone()

            builder.push(builder.encode(answer), supervise=True)
            builder.push([builder.eos], supervise=True)

            return builder.build()

        prompt_input_ids, _ = prefix.build()
        chosen_input_ids, chosen_labels = build_answer(chosen)
        rejected_input_ids, rejected_labels = build_answer(rejected)

        return prompt_input_ids, chosen_input_ids, chosen_labels, rejected_input_ids, rejected_labels
