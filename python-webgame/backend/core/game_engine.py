"""
Mirror Maze Game Engine
핵심 게임 로직 처리
"""
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import math

class CellType(Enum):
    EMPTY = "empty"
    WALL = "wall"
    MIRROR_LEFT = "mirror_left"    # \ 방향 거울
    MIRROR_RIGHT = "mirror_right"  # / 방향 거울
    SPLITTER = "splitter"          # 빔 분할기
    FILTER_RED = "filter_red"      # 빨간색 필터
    FILTER_BLUE = "filter_blue"    # 파란색 필터
    FILTER_GREEN = "filter_green"  # 초록색 필터
    PRISM = "prism"                # 프리즘 (색 분리)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class BeamColor(Enum):
    WHITE = "white"
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"   # Red + Green
    CYAN = "cyan"       # Blue + Green
    MAGENTA = "magenta" # Red + Blue

@dataclass
class LightBeam:
    """빛 빔 클래스"""
    x: int
    y: int
    direction: Direction
    color: BeamColor
    intensity: float = 1.0
    path: List[Tuple[int, int]] = field(default_factory=list)

@dataclass
class Emitter:
    """빛 발생기"""
    x: int
    y: int
    direction: Direction
    color: BeamColor
    active: bool = True

@dataclass
class Target:
    """목표 지점"""
    x: int
    y: int
    required_color: BeamColor
    is_hit: bool = False

@dataclass
class GameState:
    """게임 상태"""
    grid: List[List[CellType]]
    emitters: List[Emitter]
    targets: List[Target]
    placed_pieces: Dict[Tuple[int, int], CellType]
    moves: int = 0
    level_id: int = 0
    is_complete: bool = False
    
    def dict(self):
        return {
            "grid": [[cell.value for cell in row] for row in self.grid],
            "emitters": [
                {"x": e.x, "y": e.y, "direction": e.direction.name, "color": e.color.value}
                for e in self.emitters
            ],
            "targets": [
                {"x": t.x, "y": t.y, "required_color": t.required_color.value, "is_hit": t.is_hit}
                for t in self.targets
            ],
            "placed_pieces": {f"{x},{y}": cell.value for (x, y), cell in self.placed_pieces.items()},
            "moves": self.moves,
            "level_id": self.level_id,
            "is_complete": self.is_complete
        }

class GameEngine:
    """게임 엔진"""
    
    def __init__(self):
        self.current_state: Optional[GameState] = None
        self.grid_size = 10
        self.current_moves = 0
        self.min_moves = 0  # 최소 이동 수 (별점 계산용)
        self.available_pieces = {}  # 사용 가능한 조각들
        
    def start_new_game(self, level_data: dict) -> GameState:
        """새 게임 시작"""
        # 그리드 초기화
        grid = [[CellType.EMPTY for _ in range(self.grid_size)] 
                for _ in range(self.grid_size)]
        
        # 벽 설정
        for wall in level_data.get("walls", []):
            grid[wall["y"]][wall["x"]] = CellType.WALL
        
        # 발광기 설정
        emitters = []
        for em_data in level_data.get("emitters", []):
            emitters.append(Emitter(
                x=em_data["x"],
                y=em_data["y"],
                direction=Direction[em_data["direction"]],
                color=BeamColor[em_data["color"]]
            ))
        
        # 타겟 설정
        targets = []
        for target_data in level_data.get("targets", []):
            targets.append(Target(
                x=target_data["x"],
                y=target_data["y"],
                required_color=BeamColor[target_data["required_color"]]
            ))
        
        # 사용 가능한 조각들
        self.available_pieces = level_data.get("available_pieces", {})
        self.min_moves = level_data.get("min_moves", 10)
        
        self.current_state = GameState(
            grid=grid,
            emitters=emitters,
            targets=targets,
            placed_pieces={},
            level_id=level_data.get("id", 0)
        )
        
        self.current_moves = 0
        return self.current_state
    
    def perform_action(self, action: str, x: int, y: int, 
                      piece_type: Optional[str] = None, 
                      rotation: Optional[int] = None) -> bool:
        """액션 수행"""
        if not self.current_state:
            return False
        
        if action == "place":
            return self._place_piece(x, y, piece_type)
        elif action == "rotate":
            return self._rotate_piece(x, y)
        elif action == "remove":
            return self._remove_piece(x, y)
        
        return False
    
    def _place_piece(self, x: int, y: int, piece_type: str) -> bool:
        """조각 배치"""
        if not self._is_valid_position(x, y):
            return False
        
        if self.current_state.grid[y][x] != CellType.EMPTY:
            return False
        
        # 사용 가능한 조각 확인
        if piece_type in self.available_pieces:
            if self.available_pieces[piece_type] <= 0:
                return False
            self.available_pieces[piece_type] -= 1
        
        try:
            cell_type = CellType(piece_type)
            self.current_state.grid[y][x] = cell_type
            self.current_state.placed_pieces[(x, y)] = cell_type
            self.current_moves += 1
            self.current_state.moves = self.current_moves
            return True
        except:
            return False
    
    def _rotate_piece(self, x: int, y: int) -> bool:
        """조각 회전"""
        if not self._is_valid_position(x, y):
            return False
        
        cell = self.current_state.grid[y][x]
        
        # 회전 가능한 조각만 회전
        if cell == CellType.MIRROR_LEFT:
            self.current_state.grid[y][x] = CellType.MIRROR_RIGHT
            self.current_moves += 1
            return True
        elif cell == CellType.MIRROR_RIGHT:
            self.current_state.grid[y][x] = CellType.MIRROR_LEFT
            self.current_moves += 1
            return True
        
        return False
    
    def _remove_piece(self, x: int, y: int) -> bool:
        """조각 제거"""
        if not self._is_valid_position(x, y):
            return False
        
        if (x, y) in self.current_state.placed_pieces:
            piece_type = self.current_state.placed_pieces[(x, y)]
            
            # 조각 반환
            if piece_type.value in self.available_pieces:
                self.available_pieces[piece_type.value] += 1
            
            self.current_state.grid[y][x] = CellType.EMPTY
            del self.current_state.placed_pieces[(x, y)]
            self.current_moves += 1
            return True
        
        return False
    
    def calculate_light_paths(self) -> List[Dict]:
        """빛 경로 계산"""
        if not self.current_state:
            return []
        
        paths = []
        
        for emitter in self.current_state.emitters:
            if not emitter.active:
                continue
            
            beam = LightBeam(
                x=emitter.x,
                y=emitter.y,
                direction=emitter.direction,
                color=emitter.color
            )
            
            beam_paths = self._trace_beam(beam)
            paths.extend(beam_paths)
        
        # 타겟 히트 체크
        self._check_targets_hit(paths)
        
        return paths
    
    def _trace_beam(self, beam: LightBeam, depth: int = 0) -> List[Dict]:
        """빔 추적"""
        if depth > 100:  # 무한 루프 방지
            return []
        
        paths = []
        current_path = []
        visited = set()
        
        x, y = beam.x, beam.y
        dx, dy = beam.direction.value
        color = beam.color
        
        while True:
            # 다음 위치로 이동
            x += dx
            y += dy
            
            # 경계 체크
            if not self._is_valid_position(x, y):
                break
            
            # 무한 루프 체크
            state = (x, y, dx, dy)
            if state in visited:
                break
            visited.add(state)
            
            current_path.append((x, y))
            cell = self.current_state.grid[y][x]
            
            # 벽에 부딪힘
            if cell == CellType.WALL:
                break
            
            # 거울 처리
            if cell == CellType.MIRROR_LEFT:  # \ 거울
                if dx == 1:  # 오른쪽으로 가던 빔
                    dx, dy = 0, 1  # 아래로
                elif dx == -1:  # 왼쪽으로 가던 빔
                    dx, dy = 0, -1  # 위로
                elif dy == 1:  # 아래로 가던 빔
                    dx, dy = 1, 0  # 오른쪽으로
                elif dy == -1:  # 위로 가던 빔
                    dx, dy = -1, 0  # 왼쪽으로
                    
            elif cell == CellType.MIRROR_RIGHT:  # / 거울
                if dx == 1:  # 오른쪽으로 가던 빔
                    dx, dy = 0, -1  # 위로
                elif dx == -1:  # 왼쪽으로 가던 빔
                    dx, dy = 0, 1  # 아래로
                elif dy == 1:  # 아래로 가던 빔
                    dx, dy = -1, 0  # 왼쪽으로
                elif dy == -1:  # 위로 가던 빔
                    dx, dy = 1, 0  # 오른쪽으로
            
            # 분할기 처리
            elif cell == CellType.SPLITTER:
                # 현재 빔 계속 진행
                new_beam1 = LightBeam(x, y, Direction((dx, dy)), color)
                paths.extend(self._trace_beam(new_beam1, depth + 1))
                
                # 90도 회전한 빔 생성
                new_dx, new_dy = -dy, dx
                new_beam2 = LightBeam(x, y, Direction((new_dx, new_dy)), color)
                paths.extend(self._trace_beam(new_beam2, depth + 1))
                break
            
            # 필터 처리
            elif cell in [CellType.FILTER_RED, CellType.FILTER_BLUE, CellType.FILTER_GREEN]:
                filter_color = cell.name.split('_')[1].lower()
                if color == BeamColor.WHITE or color.value == filter_color:
                    color = BeamColor[filter_color.upper()]
                else:
                    break  # 필터를 통과할 수 없음
            
            # 프리즘 처리
            elif cell == CellType.PRISM and color == BeamColor.WHITE:
                # 백색광을 RGB로 분리
                for new_color in [BeamColor.RED, BeamColor.GREEN, BeamColor.BLUE]:
                    angle_offset = [-1, 0, 1][["RED", "GREEN", "BLUE"].index(new_color.name)]
                    new_dx = dx + angle_offset * dy
                    new_dy = dy - angle_offset * dx
                    if new_dx != 0 or new_dy != 0:
                        new_beam = LightBeam(x, y, Direction((new_dx, new_dy)), new_color)
                        paths.extend(self._trace_beam(new_beam, depth + 1))
                break
        
        if current_path:
            paths.append({
                "path": current_path,
                "color": color.value,
                "start": (beam.x, beam.y),
                "end": current_path[-1] if current_path else (beam.x, beam.y)
            })
        
        return paths
    
    def _check_targets_hit(self, paths: List[Dict]):
        """타겟 히트 체크"""
        # 모든 타겟 초기화
        for target in self.current_state.targets:
            target.is_hit = False
        
        # 경로상의 타겟 체크
        for path_data in paths:
            for x, y in path_data["path"]:
                for target in self.current_state.targets:
                    if target.x == x and target.y == y:
                        if path_data["color"] == target.required_color.value:
                            target.is_hit = True
    
    def check_victory(self) -> bool:
        """승리 조건 체크"""
        if not self.current_state:
            return False
        
        all_hit = all(target.is_hit for target in self.current_state.targets)
        self.current_state.is_complete = all_hit
        return all_hit
    
    def calculate_stars(self) -> int:
        """별점 계산"""
        if not self.check_victory():
            return 0
        
        ratio = self.current_moves / self.min_moves if self.min_moves > 0 else 1
        
        if ratio <= 1.0:
            return 3
        elif ratio <= 1.5:
            return 2
        else:
            return 1
    
    def get_hint(self) -> Optional[str]:
        """힌트 제공"""
        if not self.current_state:
            return None
        
        # 간단한 힌트 시스템
        unhit_targets = [t for t in self.current_state.targets if not t.is_hit]
        if unhit_targets:
            target = unhit_targets[0]
            return f"Try to guide {target.required_color.value} light to position ({target.x}, {target.y})"
        
        return "Check if all mirrors are positioned correctly"
    
    def _is_valid_position(self, x: int, y: int) -> bool:
        """유효한 위치인지 확인"""
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size
    
    def get_current_state(self) -> GameState:
        """현재 게임 상태 반환"""
        return self.current_state