from __future__ import annotations

import argparse
from typing import List

from src.data import create_default_team, create_sample_enemy
from src.encounter import Encounter


def render(log: List[str]) -> None:
    for line in log:
        print(line)


def interactive_loop(encounter: Encounter) -> None:
    print("输入指令: attack / skill / dodge / resonance / switch <idx>")
    while not encounter.is_over():
        print("\n".join(encounter.log_state()))
        command = input("选择动作: ").strip().split()
        if not command:
            continue
        action = command[0]
        target_index = int(command[1]) if len(command) > 1 else 0
        render(encounter.player_turn(action, target_index=target_index))
        if encounter.is_over():
            break
        render(encounter.enemy_turn())

    result = "胜利" if encounter.enemy.alive is False else "失败"
    print(f"\n战斗结束: {result}")


def demo_run() -> None:
    encounter = Encounter(create_default_team(), create_sample_enemy())
    log, enemy_alive = encounter.auto_script()
    render(encounter.log_state())
    render(log)
    result = "胜利" if not enemy_alive else "未击破，仍可继续扩展玩法"\
        "（可切换到互动模式）。"
    print(f"\n战斗结果: {result}")


def main() -> None:
    parser = argparse.ArgumentParser(description="简易鸣潮风格动作 RPG 文本原型")
    parser.add_argument("--demo", action="store_true", help="运行预设脚本展示")
    args = parser.parse_args()

    encounter = Encounter(create_default_team(), create_sample_enemy())
    if args.demo:
        demo_run()
    else:
        interactive_loop(encounter)


if __name__ == "__main__":
    main()
