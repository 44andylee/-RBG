from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Character:
    """A lightweight representation of a playable character.

    The model is intentionally small but leaves extension points for adding
    modifiers, buffs, or elemental tags later on.
    """

    name: str
    max_hp: int
    attack: int
    defense: int
    energy: int = 0
    max_energy: int = 100
    dodge_cooldown: int = 0
    skill_cooldown: int = 0
    hp: int = field(init=False)
    action_log: List[str] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.hp = self.max_hp

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def gain_energy(self, amount: int) -> None:
        self.energy = min(self.max_energy, self.energy + amount)

    def take_damage(self, amount: int) -> int:
        damage = max(1, amount - self.defense)
        self.hp = max(0, self.hp - damage)
        return damage

    def heal(self, amount: int) -> int:
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def start_turn(self) -> None:
        """Reduce cooldowns at the beginning of a player turn."""
        self.dodge_cooldown = max(0, self.dodge_cooldown - 1)
        self.skill_cooldown = max(0, self.skill_cooldown - 1)

    def log(self, message: str) -> None:
        self.action_log.append(message)

    def flush_log(self) -> List[str]:
        log, self.action_log = self.action_log, []
        return log
