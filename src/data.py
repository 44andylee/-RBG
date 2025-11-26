from __future__ import annotations

from .character import Character
from .enemy import Enemy
from .team import Team


def create_default_team() -> Team:
    duelist = Character(name="凌锋·太刀", max_hp=120, attack=24, defense=6)
    striker = Character(name="白芷·拳刃", max_hp=110, attack=22, defense=7)
    caster = Character(name="雾灵·音律", max_hp=90, attack=28, defense=5)
    return Team([duelist, striker, caster])


def create_sample_enemy() -> Enemy:
    return Enemy(name="遗迹哨兵", max_hp=200, attack=18, defense=4, toughness=40)
