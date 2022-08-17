from dataclasses import dataclass

@dataclass
class GameConfig:
        code_length:    int
        symbol_count:   int
        doublons:       bool = True
    # ###############################################
