"""
Game Models - 데이터 모델 정의
"""
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class Level(BaseModel):
    """레벨 모델"""
    id: int
    name: str
    difficulty: str
    description: str
    grid_size: int
    min_moves: int
    walls: List[Dict[str, int]]
    emitters: List[Dict]
    targets: List[Dict]
    available_pieces: Dict[str, int]
    
class Move(BaseModel):
    """이동 기록 모델"""
    action: str
    x: int
    y: int
    piece_type: Optional[str] = None
    timestamp: datetime = datetime.now()
    
class PlayerProgress(BaseModel):
    """플레이어 진행상황"""
    player_id: str
    level_id: int
    completed: bool
    stars: int
    moves: int
    best_moves: int
    play_time: int  # seconds
    
class GameSave(BaseModel):
    """게임 저장 데이터"""
    save_id: str
    player_id: str
    level_id: int
    grid_state: List[List[str]]
    placed_pieces: Dict[str, str]
    moves: List[Move]
    timestamp: datetime = datetime.now()