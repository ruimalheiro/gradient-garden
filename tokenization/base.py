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
