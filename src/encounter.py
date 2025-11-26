from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple

from .character import Character, StatusEffect
from .enemy import Enemy
from .team import Team

ActionLog = List[str]


@dataclass
class Encounter:
    team: Team
    enemy: Enemy
    dodge_window: bool = False

    def log_state(self) -> List[str]:
        status = [
            f"敌人 {self.enemy.name}: HP {self.enemy.hp}/{self.enemy.max_hp} | 韧性 {self.enemy.toughness}",
        ]
        for i, c in enumerate(self.team.members):
            prefix = "*" if i == self.team.active_index else " "
            status.append(
                f"{prefix} {c.name}: HP {c.hp}/{c.max_hp} | 能量 {c.energy}/{c.max_energy} | 技能CD {c.skill_cooldown} | 闪避CD {c.dodge_cooldown}"
            )
        return status

    def player_turn(self, action: str, target_index: int = 0) -> ActionLog:
        actor = self.team.active
        log: ActionLog = actor.start_turn()

        if action == "attack":
            dmg = self.enemy.take_damage(actor.attack_value, toughness_break=5)
            actor.gain_energy(10)
            log.append(f"{actor.name} 使用普攻造成 {dmg} 伤害，削韧 5。")
        elif action == "skill":
            if actor.skill_cooldown > 0:
                log.append("技能冷却中！")
            else:
                log.extend(self.perform_unique_skill(actor))
        elif action == "dodge":
            if actor.dodge_cooldown > 0:
                log.append("闪避未冷却，动作失败！")
            else:
                self.dodge_window = True
                actor.dodge_cooldown = 1
                actor.gain_energy(12)
                log.append(f"{actor.name} 精准闪避，进入反击窗口并获得能量。")
        elif action == "switch":
            message = self.team.switch(target_index)
            log.append(message)
            if "援护" in message:
                swapped = self.team.active
                sub_dmg = self.enemy.take_damage(int(swapped.attack_value * 0.8), toughness_break=8)
                log.append(f"援护击造成 {sub_dmg} 伤害并削韧。")
        elif action == "resonance":
            if actor.energy < actor.max_energy:
                log.append("能量不足，无法释放共鸣解放。")
            else:
                dmg = self.enemy.take_damage(actor.attack_value * 3, toughness_break=20)
                actor.energy = 0
                log.append(f"{actor.name} 释放共鸣解放，爆发造成 {dmg} 伤害！")
        else:
            log.append("未知指令。")

        return log + actor.flush_log() + self.enemy.flush_log()

    def enemy_turn(self) -> ActionLog:
        log: ActionLog = []
        actor = self.team.active

        if not self.enemy.alive:
            return ["敌人已被击败！"]

        self.enemy.start_turn()

        # If staggered, enemy skips attacking this turn
        if self.enemy.staggered:
            log.append(f"{self.enemy.name} 处于硬直，无法行动。")
            return log + self.enemy.flush_log()

        # Enemy attack
        raw_damage = self.enemy.attack + random.randint(-2, 2)
        if self.dodge_window:
            self.dodge_window = False
            actor.gain_energy(15)
            log.append(f"{actor.name} 成功闪避，获得反击能量！")
            counter_damage = self.enemy.take_damage(int(actor.attack_value * 1.2), toughness_break=6)
            log.append(f"闪避反击造成 {counter_damage} 伤害并削韧。")
        else:
            if self.enemy.heavy_prepared:
                raw_damage += 6
                self.enemy.heavy_prepared = False
                damage = actor.take_damage(raw_damage)
                actor.apply_status(StatusEffect(name="流血", value=4, duration=2, kind="dot"))
                log.append(f"{self.enemy.name} 的重击造成 {damage} 点伤害，并附加流血！")
            else:
                damage = actor.take_damage(raw_damage)
                log.append(f"{self.enemy.name} 造成 {damage} 点伤害。")

        return log + actor.flush_log() + self.enemy.flush_log()

    def perform_unique_skill(self, actor: Character) -> ActionLog:
        log: ActionLog = []
        # default energy gain
        energy_gain = 18
        if "凌锋" in actor.name:
            hit1 = self.enemy.take_damage(int(actor.attack_value * 0.9), toughness_break=6)
            hit2 = self.enemy.take_damage(int(actor.attack_value * 1.1), toughness_break=8)
            actor.skill_cooldown = 2
            log.append(f"{actor.name} 双段斩击造成 {hit1 + hit2} 伤害并大幅削韧。")
        elif "白芷" in actor.name:
            buff = StatusEffect(name="攻刃强化", value=6, duration=2, kind="buff")
            actor.apply_status(buff)
            self.enemy.take_damage(int(actor.attack_value * 0.8), toughness_break=6)
            actor.skill_cooldown = 3
            energy_gain = 16
            log.append(f"{actor.name} 强化拳刃，获得攻击力提升并造成额外伤害。")
        elif "雾灵" in actor.name:
            healed_total = 0
            for member in self.team.alive_members:
                healed_total += member.heal(12)
            actor.skill_cooldown = 2
            energy_gain = 14
            log.append(f"{actor.name} 演奏共鸣，为队伍恢复 {healed_total} 点生命。")
        else:
            damage = self.enemy.take_damage(int(actor.attack_value * 1.6), toughness_break=10)
            actor.skill_cooldown = 2
            log.append(f"{actor.name} 释放共鸣战技，造成 {damage} 伤害并削韧。")

        actor.gain_energy(energy_gain)
        return log

    def is_over(self) -> bool:
        return not self.enemy.alive or not self.team.any_alive()

    def auto_script(self) -> Tuple[List[str], bool]:
        """Run a deterministic script for demo purposes."""
        script = [
            ("attack", None),
            ("dodge", None),
            ("skill", None),
            ("switch", 1),
            ("attack", None),
            ("resonance", None),
        ]
        log: List[str] = []
        for action, index in script:
            if self.is_over():
                break
            log.append(f"\n=== {self.team.active.name} 行动: {action} ===")
            log.extend(self.player_turn(action, target_index=index or 0))
            if self.is_over():
                break
            log.extend(self.enemy_turn())
        return log, self.enemy.alive
