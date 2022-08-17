from dataclasses import dataclass
from collections import Counter
# ###############################################
from .code import Code
# ###############################################


@dataclass
class Hash:
    wp: int
    ip: int
    # ###############################################

    def __str__(self) -> str:
        return '%d%d' % (self.wp, self.ip)
    # ###############################################

    @classmethod
    def compute(cls, c0: Code, c1: Code):
        # well-placed counter
        wp = (c0.value == c1.value).sum()
        # ill-placed counter
        cnt_0 = Counter(c0.value)
        cnt_1 = Counter(c1.value)
        ip    = sum([
            min(v0, cnt_1.get(k0, 0))
            for k0, v0 in cnt_0.items()
        ]) - wp
        
        return cls(wp, ip)
    # ###############################################
