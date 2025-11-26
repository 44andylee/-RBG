# -RBG

《鸣潮》风格的开放世界动作 RPG 设计草案 + 终端原型。

- 设计文档：查看 [docs/design.md](docs/design.md)。
- 试玩原型：`python main.py --demo` 查看预设战斗脚本，或运行 `python main.py` 进入交互模式（支持 attack / skill / dodge / resonance / switch <idx>）。
- 机制亮点：
  - 敌人蓄力重击 + 硬直韧性：精准闪避可反击，未闪避会被附加流血。
  - 角色定制战技：凌锋双段破韧，白芷强化攻刃，雾灵团队回复。
  - Buff / DoT 支持：状态随回合衰减，能量与冷却循环更贴近动作 RPG 节奏。
