/**
 * Mirror Maze Game Logic
 */

class MirrorMazeGame {
    constructor() {
        this.currentLevel = null;
        this.levelId = 1;
        this.gameState = null;
        this.selectedTool = null;
        this.currentAction = 'place'; // place, rotate, remove
        this.moves = 0;
        this.lightPaths = [];
        this.availablePieces = {};
        this.soundEnabled = true;
        
        this.apiUrl = 'http://localhost:8000/api';
    }
    
    async init() {
        await this.loadLevels();
        this.setupEventListeners();
    }
    
    async loadLevels() {
        try {
            const response = await fetch(`${this.apiUrl}/levels`);
            this.levels = await response.json();
            this.renderLevelSelect();
        } catch (error) {
            console.error('Failed to load levels:', error);
        }
    }
    
    renderLevelSelect() {
        const grid = document.getElementById('level-grid');
        grid.innerHTML = '';
        
        this.levels.forEach((level, index) => {
            const card = document.createElement('div');
            card.className = 'level-card';
            if (index > 0 && !this.isLevelUnlocked(level.id)) {
                card.classList.add('locked');
            }
            
            card.innerHTML = `
                <div class="level-number">${level.id}</div>
                <div class="level-card-name">${level.name}</div>
                <div class="level-difficulty">${level.difficulty}</div>
                <div class="level-stars">
                    ${this.renderStars(level.stars || 0)}
                </div>
            `;
            
            if (!card.classList.contains('locked')) {
                card.addEventListener('click', () => this.startLevel(level.id));
            }
            
            grid.appendChild(card);
        });
    }
    
    renderStars(count) {
        let stars = '';
        for (let i = 0; i < 3; i++) {
            stars += `<span class="star ${i < count ? '' : 'empty'}">⭐</span>`;
        }
        return stars;
    }
    
    isLevelUnlocked(levelId) {
        // 첫 번째 레벨은 항상 열려있음
        if (levelId === 1) return true;
        
        // localStorage에서 진행상황 확인
        const progress = JSON.parse(localStorage.getItem('mirrorMazeProgress') || '{}');
        return progress[levelId - 1]?.completed || false;
    }
    
    async startLevel(levelId) {
        try {
            const response = await fetch(`${this.apiUrl}/game/start/${levelId}`, {
                method: 'POST'
            });
            const data = await response.json();
            
            this.levelId = levelId;
            this.gameState = data.game_state;
            this.moves = 0;
            
            // 레벨 데이터 로드
            const levelResponse = await fetch(`${this.apiUrl}/levels/${levelId}`);
            this.currentLevel = await levelResponse.json();
            
            this.availablePieces = {...this.currentLevel.available_pieces};
            
            // UI 전환
            this.switchScreen('game-screen');
            this.updateUI();
            this.render();
            
            // 도구 업데이트
            this.updateTools();
            
        } catch (error) {
            console.error('Failed to start level:', error);
        }
    }
    
    switchScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }
    
    updateUI() {
        if (!this.currentLevel) return;
        
        document.getElementById('current-level').textContent = this.levelId;
        document.getElementById('move-count').textContent = this.moves;
        document.getElementById('level-name').textContent = this.currentLevel.name;
        document.getElementById('level-description').textContent = this.currentLevel.description;
        document.getElementById('difficulty').textContent = this.currentLevel.difficulty;
        document.getElementById('min-moves').textContent = this.currentLevel.min_moves;
    }
    
    updateTools() {
        const tools = document.querySelectorAll('.tool');
        tools.forEach(tool => {
            const toolType = tool.dataset.tool;
            const count = this.availablePieces[toolType] || 0;
            const countElement = tool.querySelector('.tool-count');
            
            countElement.textContent = count;
            
            if (count === 0) {
                tool.classList.add('disabled');
            } else {
                tool.classList.remove('disabled');
            }
        });
    }
    
    setupEventListeners() {
        // 도구 선택
        document.querySelectorAll('.tool').forEach(tool => {
            tool.addEventListener('click', () => {
                if (!tool.classList.contains('disabled')) {
                    this.selectTool(tool.dataset.tool);
                    
                    // UI 업데이트
                    document.querySelectorAll('.tool').forEach(t => t.classList.remove('selected'));
                    tool.classList.add('selected');
                    
                    this.currentAction = 'place';
                    this.updateActionButtons();
                }
            });
        });
        
        // 액션 버튼
        document.getElementById('rotate-btn').addEventListener('click', () => {
            this.currentAction = 'rotate';
            this.selectedTool = null;
            this.updateActionButtons();
            document.querySelectorAll('.tool').forEach(t => t.classList.remove('selected'));
        });
        
        document.getElementById('remove-btn').addEventListener('click', () => {
            this.currentAction = 'remove';
            this.selectedTool = null;
            this.updateActionButtons();
            document.querySelectorAll('.tool').forEach(t => t.classList.remove('selected'));
        });
        
        // 컨트롤 버튼
        document.getElementById('check-solution').addEventListener('click', () => {
            this.checkSolution();
        });
        
        document.getElementById('reset-level').addEventListener('click', () => {
            this.resetLevel();
        });
        
        document.getElementById('hint-btn').addEventListener('click', () => {
            this.showHint();
        });
        
        document.getElementById('back-to-menu').addEventListener('click', () => {
            this.switchScreen('level-select');
        });
        
        // 승리 화면 버튼
        document.getElementById('next-level').addEventListener('click', () => {
            this.startLevel(this.levelId + 1);
            document.getElementById('victory-screen').classList.remove('active');
        });
        
        document.getElementById('replay-level').addEventListener('click', () => {
            this.resetLevel();
            document.getElementById('victory-screen').classList.remove('active');
        });
        
        document.getElementById('menu-from-victory').addEventListener('click', () => {
            document.getElementById('victory-screen').classList.remove('active');
            this.switchScreen('level-select');
            this.loadLevels();
        });
        
        // 사운드 토글
        document.getElementById('sound-toggle').addEventListener('click', () => {
            this.soundEnabled = !this.soundEnabled;
            document.getElementById('sound-icon').textContent = this.soundEnabled ? '🔊' : '🔇';
        });
        
        // 캔버스 클릭
        const canvas = document.getElementById('game-canvas');
        canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        canvas.addEventListener('mousemove', (e) => this.handleCanvasHover(e));
        
        // 키보드 단축키
        document.addEventListener('keydown', (e) => {
            if (e.key === 'r' || e.key === 'R') {
                this.currentAction = 'rotate';
                this.updateActionButtons();
            } else if (e.key === 'Delete' || e.key === 'Backspace') {
                this.currentAction = 'remove';
                this.updateActionButtons();
            } else if (e.key === 'Escape') {
                this.currentAction = 'place';
                this.selectedTool = null;
                this.updateActionButtons();
                document.querySelectorAll('.tool').forEach(t => t.classList.remove('selected'));
            }
        });
    }
    
    updateActionButtons() {
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        if (this.currentAction === 'rotate') {
            document.getElementById('rotate-btn').classList.add('active');
        } else if (this.currentAction === 'remove') {
            document.getElementById('remove-btn').classList.add('active');
        }
    }
    
    selectTool(toolType) {
        this.selectedTool = toolType;
    }
    
    async handleCanvasClick(event) {
        const canvas = document.getElementById('game-canvas');
        const rect = canvas.getBoundingClientRect();
        const x = Math.floor((event.clientX - rect.left) / 50);
        const y = Math.floor((event.clientY - rect.top) / 50);
        
        if (x < 0 || x >= 10 || y < 0 || y >= 10) return;
        
        try {
            const response = await fetch(`${this.apiUrl}/game/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: this.currentAction,
                    x: x,
                    y: y,
                    piece_type: this.selectedTool
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.gameState = data.game_state;
                this.lightPaths = data.light_paths;
                this.moves = data.moves;
                
                // 도구 카운트 업데이트
                if (this.currentAction === 'place' && this.selectedTool) {
                    this.availablePieces[this.selectedTool]--;
                } else if (this.currentAction === 'remove') {
                    // 제거된 조각 복구
                    const removedPiece = data.removed_piece;
                    if (removedPiece && this.availablePieces[removedPiece] !== undefined) {
                        this.availablePieces[removedPiece]++;
                    }
                }
                
                this.updateUI();
                this.updateTools();
                this.render();
                
                if (data.is_complete) {
                    this.showVictory(data.stars);
                }
                
                // 효과음
                if (this.soundEnabled) {
                    this.playSound('place');
                }
            }
        } catch (error) {
            console.error('Failed to perform action:', error);
        }
    }
    
    handleCanvasHover(event) {
        // 호버 효과 구현
        const canvas = document.getElementById('game-canvas');
        const rect = canvas.getBoundingClientRect();
        const x = Math.floor((event.clientX - rect.left) / 50);
        const y = Math.floor((event.clientY - rect.top) / 50);
        
        // 호버 위치를 렌더러에 전달
        if (window.renderer) {
            window.renderer.setHoverPosition(x, y);
            window.renderer.render();
        }
    }
    
    async checkSolution() {
        // 빛 경로 계산 및 확인
        const response = await fetch(`${this.apiUrl}/game/action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: 'check',
                x: 0,
                y: 0
            })
        });
        
        const data = await response.json();
        this.lightPaths = data.light_paths;
        this.render();
        
        if (data.is_complete) {
            this.showVictory(data.stars);
        }
    }
    
    async resetLevel() {
        await this.startLevel(this.levelId);
    }
    
    async showHint() {
        try {
            const response = await fetch(`${this.apiUrl}/game/hint/${this.levelId}`);
            const data = await response.json();
            
            const hintDisplay = document.getElementById('hint-display');
            hintDisplay.textContent = data.hint;
            hintDisplay.classList.add('active');
            
            setTimeout(() => {
                hintDisplay.classList.remove('active');
            }, 5000);
        } catch (error) {
            console.error('Failed to get hint:', error);
        }
    }
    
    showVictory(stars) {
        // 진행상황 저장
        const progress = JSON.parse(localStorage.getItem('mirrorMazeProgress') || '{}');
        progress[this.levelId] = {
            completed: true,
            stars: stars,
            moves: this.moves
        };
        localStorage.setItem('mirrorMazeProgress', JSON.stringify(progress));
        
        // 승리 화면 표시
        document.getElementById('victory-screen').classList.add('active');
        document.getElementById('final-moves').textContent = this.moves;
        document.getElementById('final-min-moves').textContent = this.currentLevel.min_moves;
        
        // 별 애니메이션
        const starElements = document.querySelectorAll('#victory-stars .star');
        starElements.forEach((star, index) => {
            setTimeout(() => {
                if (index < stars) {
                    star.style.color = '#ffd700';
                } else {
                    star.style.color = 'rgba(255, 255, 255, 0.3)';
                }
                star.classList.add('animate');
            }, index * 300);
        });
        
        if (this.soundEnabled) {
            this.playSound('victory');
        }
    }
    
    playSound(type) {
        // 사운드 재생 (실제 구현 시 오디오 파일 필요)
        console.log(`Playing sound: ${type}`);
    }
    
    render() {
        if (window.renderer) {
            window.renderer.updateGameState(this.gameState, this.lightPaths);
            window.renderer.render();
        }
    }
}

// 게임 인스턴스 생성
window.game = new MirrorMazeGame();