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
        self.eos_id = tokenizer.eos_id
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

    def add_message(self, role, content, *, supervise=False, end_turn=False):
        prefix = self.role_prefix(role)
        self.push(self.encode(prefix), supervise=False)

        if role == 'assistant':
            self.push(self.encode(content), supervise=supervise)

            if end_turn:
                self.push([self.eos_id], supervise=supervise)
            else:
                self.push(self.encode('\n'), supervise=supervise)
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
    def encode(self, text):
        ...

    @abstractmethod
    def decode(self, ids):
        ...

    def encode_instruct_messages_inference(self, messages):
        builder = PromptBuilder(self, no_labels=True)

        for message in messages:
            role = message['role']

            builder.add_message(
                role,
                message['content'],
                end_turn=(role == "assistant")
            )

        builder.add_assistant_prefix()

        return builder.build()

    def encode_instruct_inference(self, text: str, system_msg: bool = True):
        messages = []

        if system_msg:
            messages.append({
                'role': 'system',
                'content': self.system_prompt,
            })

        messages.append({
            'role': 'user',
            'content': text,
        })

        return self.encode_instruct_messages_inference(messages)

    def validate_conversation(
        self,
        conversation,
        *,
        expected_last_role,
    ):
        if not conversation:
            raise ValueError('Conversation cannot be empty')

        if conversation[-1]['role'] != expected_last_role:
            raise ValueError(
                f'Conversation must end with {expected_last_role}, '
                f'got {conversation[-1]["role"]}'
            )

        expected_role = 'user'

        for index, message in enumerate(conversation):
            role = message['role']

            if role not in {'user', 'assistant'}:
                raise ValueError(
                    f'Unexpected role at index {index}: {role}. '
                    'System messages must be passed through system_prompt.'
                )

            if role != expected_role:
                raise ValueError(
                    f'Expected {expected_role} at index {index}, got {role}'
                )

            expected_role = (
                'assistant'
                if expected_role == 'user'
                else 'user'
            )

    def encode_instruct_chat(
        self,
        *,
        conversation,
        ignore_index: int,
        system_prompt: str | None = None,
        max_seq_len: int | None = None,
        trim_to_context: bool = False
    ):
        self.validate_conversation(conversation, expected_last_role='assistant')

        system_prompt = (
            self.system_prompt
            if system_prompt is None
            else system_prompt
        )

        def encode_messages(messages):
            builder = PromptBuilder(self, ignore_index=ignore_index)
            builder.add_message('system', system_prompt)

            for interaction in messages:
                role = interaction['role']
                content = interaction['content']
                is_assistant = role == 'assistant'

                builder.add_message(
                    role,
                    content,
                    supervise=is_assistant,
                    end_turn=is_assistant
                )

            return builder.build()

        if trim_to_context:
            if max_seq_len is None:
                raise ValueError('max_seq_len is required when trim_to_context=True')

            messages = [m for m in conversation]
            valid_messages = []
            tokens = []
            labels = []
            while len(messages) >= 2:
                assistant = messages.pop()
                user = messages.pop()

                candidate_tokens, candidate_labels = encode_messages([user, assistant, *valid_messages])
                if len(candidate_tokens) > max_seq_len:
                    break

                valid_messages = [user, assistant, *valid_messages]
                tokens = candidate_tokens
                labels = candidate_labels

            return tokens, labels

        tokens, labels = encode_messages(conversation)

        if max_seq_len is not None and len(tokens) > max_seq_len:
            raise ValueError(
                f'Encoded instruct example length {len(tokens)} exceeds max_seq_len={max_seq_len}'
            )

        return tokens, labels

    def encode_instruct_chat_dpo(
        self,
        *,
        conversation,
        chosen: str,
        rejected: str,
        ignore_index: int,
        system_prompt: str | None = None,
        max_seq_len: int | None = None,
        trim_to_context: bool = False
    ):
        self.validate_conversation(conversation, expected_last_role='user')

        system_prompt = (
            self.system_prompt
            if system_prompt is None
            else system_prompt
        )

        def encode_prompt(messages):
            prefix_builder = PromptBuilder(self, ignore_index=ignore_index)
            prefix_builder.add_message('system', system_prompt)

            for interaction in messages:
                role = interaction['role']

                prefix_builder.add_message(
                    role,
                    interaction['content'],
                    supervise=False,
                    end_turn=(role == 'assistant')
                )

            prefix_builder.add_assistant_prefix()

            def build_answer(answer):
                builder = prefix_builder.clone()
                builder.push(builder.encode(answer), supervise=True)
                builder.push([builder.eos_id], supervise=True)
                return builder.build()

            prompt_ids, _ = prefix_builder.build()
            chosen_ids, chosen_labels = build_answer(chosen)
            rejected_ids, rejected_labels = build_answer(rejected)

            return prompt_ids, chosen_ids, chosen_labels, rejected_ids, rejected_labels

        def fits(prompt_tokens, chosen_tokens, rejected_tokens):
            return (
                len(prompt_tokens) <= max_seq_len and
                len(chosen_tokens) <= max_seq_len and
                len(rejected_tokens) <= max_seq_len
            )

        if trim_to_context:
            if max_seq_len is None:
                raise ValueError('max_seq_len is required when trim_to_context=True')

            messages = [m for m in conversation]
            valid_messages = [messages.pop()] # last is always user
            (
                prompt_tokens,
                chosen_tokens,
                chosen_labels,
                rejected_tokens,
                rejected_labels
            ) = encode_prompt(valid_messages)

            if not fits(prompt_tokens, chosen_tokens, rejected_tokens):
                return [], [], [], [], []

            while len(messages) >= 2:
                assistant = messages.pop()
                user = messages.pop()

                candidate_messages = [user, assistant, *valid_messages]

                (
                    candidate_prompt_tokens,
                    candidate_chosen_tokens,
                    candidate_chosen_labels,
                    candidate_rejected_tokens,
                    candidate_rejected_labels
                ) = encode_prompt(candidate_messages)
                if not fits(
                    candidate_prompt_tokens,
                    candidate_chosen_tokens,
                    candidate_rejected_tokens
                ):
                    break

                valid_messages = candidate_messages
                prompt_tokens = candidate_prompt_tokens
                chosen_tokens = candidate_chosen_tokens
                chosen_labels = candidate_chosen_labels
                rejected_tokens = candidate_rejected_tokens
                rejected_labels = candidate_rejected_labels

            return prompt_tokens, chosen_tokens, chosen_labels, rejected_tokens, rejected_labels

        prompt_tokens, chosen_tokens, chosen_labels, rejected_tokens, rejected_labels = encode_prompt(conversation)

        if max_seq_len is not None:
            if (
                len(prompt_tokens) > max_seq_len or
                len(chosen_tokens) > max_seq_len or
                len(rejected_tokens) > max_seq_len
            ):
                raise ValueError(
                    f'Encoded DPO example exceeds max_seq_len={max_seq_len}: '
                    f'prompt={len(prompt_tokens)}, chosen={len(chosen_tokens)}, rejected={len(rejected_tokens)}'
                )

        return prompt_tokens, chosen_tokens, chosen_labels, rejected_tokens, rejected_labels
