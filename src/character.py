from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class StatusEffect:
    name: str
    value: int
    duration: int
    kind: str  # "buff" or "dot"


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
    status_effects: List[StatusEffect] = field(default_factory=list)
    action_log: List[str] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.hp = self.max_hp

    @property
    def alive(self) -> bool:
        return self.hp > 0

    @property
    def attack_value(self) -> int:
        bonus = sum(effect.value for effect in self.status_effects if effect.kind == "buff")
        return self.attack + bonus

    def take_damage(self, amount: int) -> int:
        damage = max(1, amount - self.defense)
        self.hp = max(0, self.hp - damage)
        return damage

    def heal(self, amount: int) -> int:
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def gain_energy(self, amount: int) -> None:
        self.energy = min(self.max_energy, self.energy + amount)

    def apply_status(self, effect: StatusEffect) -> None:
        self.status_effects.append(effect)

    def start_turn(self) -> List[str]:
        """Reduce cooldowns and tick status effects at the beginning of a player turn."""
        self.dodge_cooldown = max(0, self.dodge_cooldown - 1)
        self.skill_cooldown = max(0, self.skill_cooldown - 1)
        logs: List[str] = []
        remaining: List[StatusEffect] = []
        for effect in self.status_effects:
            if effect.kind == "dot":
                self.hp = max(0, self.hp - effect.value)
                logs.append(f"{self.name} 受到 {effect.value} 点持续伤害（{effect.name}）。")
            effect.duration -= 1
            if effect.duration > 0:
                remaining.append(effect)
            else:
                logs.append(f"{self.name} 的 {effect.name} 结束。")
        self.status_effects = remaining
        return logs

    def log(self, message: str) -> None:
        self.action_log.append(message)

    def flush_log(self) -> List[str]:
        log, self.action_log = self.action_log, []
        return log
