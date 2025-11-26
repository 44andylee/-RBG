from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Enemy:
    name: str
    max_hp: int
    attack: int
    defense: int
    toughness: int = 40
    hp: int = None
    staggered: bool = False
    action_log: List[str] = None

    def __post_init__(self) -> None:
        self.hp = self.max_hp
        self.action_log = []

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int, toughness_break: int = 0) -> int:
        damage = max(1, amount - self.defense)
        self.hp = max(0, self.hp - damage)
        if toughness_break:
            self.toughness = max(0, self.toughness - toughness_break)
            if self.toughness == 0:
                self.staggered = True
        return damage

    def recover_toughness(self, amount: int = 10) -> None:
        if not self.staggered:
            self.toughness = min(40, self.toughness + amount)

    def start_turn(self) -> None:
        if self.staggered:
            # one free turn for the player after breaking the enemy
            self.staggered = False
            self.toughness = 20
            self.action_log.append(f"{self.name} 从硬直中恢复，韧性重置为 20。")
        else:
            self.recover_toughness(5)

    def log(self, message: str) -> None:
        self.action_log.append(message)

    def flush_log(self) -> List[str]:
        log, self.action_log = self.action_log, []
        return log
