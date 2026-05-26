from abc import ABC, abstractmethod


class BaseTokenizer(ABC):

    @abstractmethod
    def encode(self, text, *, bos=False, eos=False, allowed_special=set(), disallowed_special=()):
        ...

    @abstractmethod
    def decode(self, ids):
        ...

    def encode_instruct(self, s, system_msg=True):
        bot = self.bos_id
        sh = self.sh_id
        eh = self.eh_id
        eot = self.eot_id

        tokens = [bot, sh]
        if system_msg:
            tokens.extend(self.encode('system'))
            tokens.extend([eh])
            tokens.extend(self.encode('\n' + self.system_prompt))
            tokens.extend([eot, sh])
        tokens.extend(self.encode('user'))
        tokens.extend([eh])
        tokens.extend(self.encode('\n'))
        tokens.extend(self.encode(s))
        tokens.extend([eot, sh])
        tokens.extend(self.encode('assistant'))
        tokens.extend([eh])
        tokens.extend(self.encode('\n'))
        return tokens

    def encode_chat(
        self,
        *,
        conversation: object,
        ignore_index: int
    ):
        bot = self.bos_id
        sh = self.sh_id
        eh = self.eh_id
        eot = self.eot_id
        eos = self.eos_id

        tokens, labels = [], []
        def push(tok_ids, is_assistant):
            tokens.extend(tok_ids)
            if is_assistant:
                labels.extend(tok_ids)
            else:
                labels.extend([ignore_index] * len(tok_ids))

        push([bot], False)
        push([sh], False)
        push(self.encode('system'), False)
        push([eh], False)
        push(self.encode('\n' + self.system_prompt), False)
        push([eot], False)

        for idx, interaction in enumerate(conversation):
            role = interaction['role']
            content = interaction['content']

            is_assistant = role == 'assistant'
            is_last_message = idx == len(conversation) - 1

            push([sh], False)
            push(self.encode(role), False)
            push([eh], False)
            push(self.encode('\n'), False)
            push(self.encode(content), is_assistant)

            if is_last_message and is_assistant:
                push([eos], True)
            else:
                push([eot], is_assistant)

        labels = labels[1:] + [ignore_index]

        return tokens, labels
