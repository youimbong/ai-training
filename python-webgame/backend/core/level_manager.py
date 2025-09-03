"""
Level Manager - 레벨 데이터 관리
"""
from typing import List, Dict, Optional
import json
from pathlib import Path

class LevelManager:
    """레벨 관리자"""
    
    def __init__(self):
        self.levels = self._load_levels()
        
    def _load_levels(self) -> Dict[int, dict]:
        """레벨 데이터 로드"""
        levels = {}
        
        # 하드코딩된 레벨 데이터 (나중에 JSON 파일로 분리 가능)
        levels[1] = {
            "id": 1,
            "name": "첫 번째 빛",
            "difficulty": "Easy",
            "description": "거울을 사용해 빛을 목표 지점으로 유도하세요",
            "grid_size": 10,
            "min_moves": 2,
            "walls": [
                {"x": 3, "y": 3}, {"x": 3, "y": 4}, {"x": 3, "y": 5},
                {"x": 6, "y": 3}, {"x": 6, "y": 4}, {"x": 6, "y": 5}
            ],
            "emitters": [
                {"x": 1, "y": 4, "direction": "RIGHT", "color": "WHITE"}
            ],
            "targets": [
                {"x": 8, "y": 4, "required_color": "WHITE"}
            ],
            "available_pieces": {
                "mirror_left": 1,
                "mirror_right": 1
            }
        }
        
        levels[2] = {
            "id": 2,
            "name": "색깔 필터",
            "difficulty": "Easy",
            "description": "필터를 사용해 올바른 색상의 빛을 만드세요",
            "grid_size": 10,
            "min_moves": 3,
            "walls": [
                {"x": 4, "y": 2}, {"x": 4, "y": 3}, {"x": 4, "y": 6}, {"x": 4, "y": 7}
            ],
            "emitters": [
                {"x": 1, "y": 5, "direction": "RIGHT", "color": "WHITE"}
            ],
            "targets": [
                {"x": 8, "y": 5, "required_color": "RED"}
            ],
            "available_pieces": {
                "filter_red": 1,
                "mirror_left": 2
            }
        }
        
        levels[3] = {
            "id": 3,
            "name": "빔 분할",
            "difficulty": "Medium",
            "description": "빔 분할기를 사용해 여러 목표를 동시에 맞추세요",
            "grid_size": 10,
            "min_moves": 4,
            "walls": [
                {"x": 5, "y": 2}, {"x": 5, "y": 7}
            ],
            "emitters": [
                {"x": 0, "y": 4, "direction": "RIGHT", "color": "WHITE"}
            ],
            "targets": [
                {"x": 9, "y": 2, "required_color": "WHITE"},
                {"x": 9, "y": 7, "required_color": "WHITE"}
            ],
            "available_pieces": {
                "splitter": 1,
                "mirror_left": 2,
                "mirror_right": 2
            }
        }
        
        levels[4] = {
            "id": 4,
            "name": "프리즘의 마법",
            "difficulty": "Medium",
            "description": "프리즘으로 백색광을 분리하여 색상별 타겟을 맞추세요",
            "grid_size": 10,
            "min_moves": 5,
            "walls": [
                {"x": 3, "y": 1}, {"x": 3, "y": 2}, {"x": 3, "y": 7}, {"x": 3, "y": 8}
            ],
            "emitters": [
                {"x": 0, "y": 4, "direction": "RIGHT", "color": "WHITE"}
            ],
            "targets": [
                {"x": 9, "y": 2, "required_color": "RED"},
                {"x": 9, "y": 4, "required_color": "GREEN"},
                {"x": 9, "y": 6, "required_color": "BLUE"}
            ],
            "available_pieces": {
                "prism": 1,
                "mirror_left": 3,
                "mirror_right": 2
            }
        }
        
        levels[5] = {
            "id": 5,
            "name": "복잡한 미로",
            "difficulty": "Hard",
            "description": "모든 도구를 활용해 복잡한 퍼즐을 해결하세요",
            "grid_size": 10,
            "min_moves": 8,
            "walls": [
                {"x": 2, "y": 2}, {"x": 2, "y": 3}, {"x": 2, "y": 6}, {"x": 2, "y": 7},
                {"x": 4, "y": 1}, {"x": 4, "y": 8}, {"x": 5, "y": 1}, {"x": 5, "y": 8},
                {"x": 7, "y": 3}, {"x": 7, "y": 4}, {"x": 7, "y": 5}, {"x": 7, "y": 6}
            ],
            "emitters": [
                {"x": 0, "y": 2, "direction": "RIGHT", "color": "WHITE"},
                {"x": 0, "y": 7, "direction": "RIGHT", "color": "WHITE"}
            ],
            "targets": [
                {"x": 9, "y": 1, "required_color": "RED"},
                {"x": 9, "y": 4, "required_color": "BLUE"},
                {"x": 9, "y": 8, "required_color": "GREEN"}
            ],
            "available_pieces": {
                "prism": 1,
                "splitter": 1,
                "mirror_left": 4,
                "mirror_right": 3,
                "filter_red": 1,
                "filter_blue": 1,
                "filter_green": 1
            }
        }
        
        levels[6] = {
            "id": 6,
            "name": "색상 혼합",
            "difficulty": "Hard",
            "description": "여러 색상을 혼합하여 새로운 색을 만들어보세요",
            "grid_size": 10,
            "min_moves": 6,
            "walls": [
                {"x": 5, "y": 3}, {"x": 5, "y": 4}, {"x": 5, "y": 5}, {"x": 5, "y": 6}
            ],
            "emitters": [
                {"x": 0, "y": 2, "direction": "RIGHT", "color": "RED"},
                {"x": 0, "y": 7, "direction": "RIGHT", "color": "GREEN"}
            ],
            "targets": [
                {"x": 9, "y": 4, "required_color": "YELLOW"}  # Red + Green = Yellow
            ],
            "available_pieces": {
                "mirror_left": 3,
                "mirror_right": 3,
                "splitter": 1
            }
        }
        
        levels[7] = {
            "id": 7,
            "name": "정밀한 각도",
            "difficulty": "Expert",
            "description": "정확한 거울 배치로 좁은 통로를 통과시키세요",
            "grid_size": 10,
            "min_moves": 10,
            "walls": [
                # 미로 형태의 벽
                {"x": 1, "y": 1}, {"x": 2, "y": 1}, {"x": 3, "y": 1}, {"x": 4, "y": 1},
                {"x": 6, "y": 1}, {"x": 7, "y": 1}, {"x": 8, "y": 1},
                {"x": 1, "y": 3}, {"x": 3, "y": 3}, {"x": 5, "y": 3}, {"x": 7, "y": 3},
                {"x": 1, "y": 5}, {"x": 3, "y": 5}, {"x": 5, "y": 5}, {"x": 7, "y": 5},
                {"x": 1, "y": 7}, {"x": 3, "y": 7}, {"x": 5, "y": 7}, {"x": 7, "y": 7},
                {"x": 1, "y": 8}, {"x": 2, "y": 8}, {"x": 3, "y": 8}, {"x": 4, "y": 8},
                {"x": 6, "y": 8}, {"x": 7, "y": 8}, {"x": 8, "y": 8}
            ],
            "emitters": [
                {"x": 0, "y": 0, "direction": "RIGHT", "color": "WHITE"}
            ],
            "targets": [
                {"x": 9, "y": 9, "required_color": "WHITE"}
            ],
            "available_pieces": {
                "mirror_left": 6,
                "mirror_right": 5
            }
        }
        
        levels[8] = {
            "id": 8,
            "name": "다중 프리즘",
            "difficulty": "Expert",
            "description": "여러 프리즘을 연쇄적으로 사용하세요",
            "grid_size": 10,
            "min_moves": 12,
            "walls": [],
            "emitters": [
                {"x": 4, "y": 0, "direction": "DOWN", "color": "WHITE"}
            ],
            "targets": [
                {"x": 0, "y": 5, "required_color": "RED"},
                {"x": 2, "y": 9, "required_color": "GREEN"},
                {"x": 7, "y": 9, "required_color": "BLUE"},
                {"x": 9, "y": 5, "required_color": "WHITE"}
            ],
            "available_pieces": {
                "prism": 2,
                "mirror_left": 5,
                "mirror_right": 5,
                "splitter": 2
            }
        }
        
        return levels
    
    def get_level(self, level_id: int) -> Optional[dict]:
        """특정 레벨 데이터 반환"""
        return self.levels.get(level_id)
    
    def get_all_levels(self) -> List[dict]:
        """모든 레벨 목록 반환"""
        return [
            {
                "id": level["id"],
                "name": level["name"],
                "difficulty": level["difficulty"],
                "description": level["description"],
                "stars": 0  # 저장된 진행상황에서 가져오기
            }
            for level in self.levels.values()
        ]
    
    def get_total_levels(self) -> int:
        """전체 레벨 수 반환"""
        return len(self.levels)
    
    def save_custom_level(self, level_data: dict) -> bool:
        """커스텀 레벨 저장"""
        try:
            level_id = max(self.levels.keys()) + 1 if self.levels else 1
            level_data["id"] = level_id
            self.levels[level_id] = level_data
            return True
        except:
            return False