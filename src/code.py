import numpy as np
from dataclasses import dataclass, field
# ###############################################

@dataclass
class Code:
    id:     int
    value:  np.ndarray = field(compare=False)
    # ###############################################

    def __repr__(self) -> str:
        return "<%s @%d '%s'>" % (
            self.__class__.__name__, self.id, self)
    # ###############################################

    def __str__(self) -> str:
        return ''.join(map(str, self.value))
    # ###############################################