from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .character import Character


@dataclass
class Team:
    members: List[Character]
    active_index: int = 0
    resonance_ready: bool = False

    @property
    def active(self) -> Character:
        return self.members[self.active_index]

    @property
    def alive_members(self) -> List[Character]:
        return [m for m in self.members if m.alive]

    def switch(self, index: int) -> Optional[str]:
        if index == self.active_index:
            return "当前已经在场。"
        if index < 0 or index >= len(self.members):
            return "无效队伍位置。"
        if not self.members[index].alive:
            return f"{self.members[index].name} 已阵亡，无法切换。"
        self.active_index = index
        return f"切换到 {self.active.name}，触发援护击！"

    def any_alive(self) -> bool:
        return any(member.alive for member in self.members)
