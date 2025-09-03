"""
Mirror Maze - 빛의 미로 퍼즐 게임
FastAPI Backend Server
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
from pathlib import Path

from backend.core.game_engine import GameEngine, GameState
from backend.core.level_manager import LevelManager
from backend.models.game_models import Level, Move, PlayerProgress

app = FastAPI(title="Mirror Maze - 빛의 미로")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game instances
game_engine = GameEngine()
level_manager = LevelManager()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

# API Models
class GameAction(BaseModel):
    action: str  # place, rotate, remove
    x: int
    y: int
    piece_type: Optional[str] = None
    rotation: Optional[int] = None

class GameSession(BaseModel):
    session_id: str
    level_id: int
    moves: int
    stars: int

# Routes
@app.get("/")
async def root():
    """게임 메인 페이지"""
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/levels")
async def get_levels():
    """모든 레벨 목록 반환"""
    return level_manager.get_all_levels()

@app.get("/api/levels/{level_id}")
async def get_level(level_id: int):
    """특정 레벨 데이터 반환"""
    level = level_manager.get_level(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level

@app.post("/api/game/start/{level_id}")
async def start_game(level_id: int):
    """새 게임 시작"""
    level = level_manager.get_level(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    
    game_state = game_engine.start_new_game(level)
    return {
        "status": "started",
        "level_id": level_id,
        "game_state": game_state.dict()
    }

@app.post("/api/game/action")
async def perform_action(action: GameAction):
    """게임 액션 수행 (거울 배치, 회전, 제거)"""
    try:
        result = game_engine.perform_action(
            action.action,
            action.x,
            action.y,
            action.piece_type,
            action.rotation
        )
        
        # 빛의 경로 재계산
        light_paths = game_engine.calculate_light_paths()
        
        # 승리 조건 체크
        is_complete = game_engine.check_victory()
        
        return {
            "success": True,
            "game_state": game_engine.get_current_state().dict(),
            "light_paths": light_paths,
            "is_complete": is_complete,
            "moves": game_engine.current_moves,
            "stars": game_engine.calculate_stars() if is_complete else 0
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/game/reset/{level_id}")
async def reset_game(level_id: int):
    """현재 레벨 리셋"""
    level = level_manager.get_level(level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    
    game_state = game_engine.start_new_game(level)
    return {
        "status": "reset",
        "level_id": level_id,
        "game_state": game_state.dict()
    }

@app.get("/api/game/hint/{level_id}")
async def get_hint(level_id: int):
    """레벨 힌트 제공"""
    hint = game_engine.get_hint()
    if not hint:
        return {"hint": "No hint available"}
    return {"hint": hint}

@app.post("/api/progress/save")
async def save_progress(session: GameSession):
    """게임 진행상황 저장"""
    # 실제로는 데이터베이스에 저장
    return {
        "status": "saved",
        "session_id": session.session_id,
        "level_id": session.level_id,
        "stars": session.stars
    }

@app.get("/api/stats")
async def get_stats():
    """게임 통계"""
    return {
        "total_levels": level_manager.get_total_levels(),
        "completed_levels": 0,  # DB에서 가져오기
        "total_stars": 0,  # DB에서 가져오기
        "total_moves": 0  # DB에서 가져오기
    }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "game": "Mirror Maze"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)