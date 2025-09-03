# Mirror Maze UX 구현 가이드

## 📱 즉시 적용 가능한 UX 개선사항

### 1. 🎯 Quick Win 개선사항 (1일 내 구현 가능)

#### 1.1 도구 선택 피드백 강화
```javascript
// frontend/js/game.js 수정
selectTool(toolType) {
    this.selectedTool = toolType;
    
    // 시각적 피드백 강화
    document.querySelectorAll('.tool').forEach(t => {
        t.classList.remove('selected', 'pulse');
    });
    
    const selectedElement = document.querySelector(`[data-tool="${toolType}"]`);
    selectedElement.classList.add('selected', 'pulse');
    
    // 커서 변경
    document.getElementById('game-canvas').style.cursor = 'crosshair';
    
    // 사운드 피드백
    this.playSound('tool-select');
    
    // 툴팁 표시
    this.showTooltip(`${toolType} 선택됨 - 보드를 클릭하여 배치`);
}
```

#### 1.2 호버 상태 개선
```css
/* frontend/css/game.css 추가 */
.tool:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
}

.tool:hover .tool-icon {
    animation: iconBounce 0.5s ease-in-out;
}

@keyframes iconBounce {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* 배치 가능 위치 표시 */
.game-cell.valid-placement {
    background: rgba(16, 185, 129, 0.2);
    border: 2px solid #10B981;
    animation: validPulse 1s infinite;
}

@keyframes validPulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}
```

#### 1.3 즉각적인 비주얼 피드백
```javascript
// 배치 성공 애니메이션
placePieceWithAnimation(x, y, pieceType) {
    const cell = this.getCellElement(x, y);
    
    // 배치 애니메이션
    cell.style.animation = 'placeSuccess 0.4s ease-out';
    
    // 파티클 효과
    this.createParticles(x, y, '#10B981', 10);
    
    // 진동 피드백 (모바일)
    if ('vibrate' in navigator) {
        navigator.vibrate(50);
    }
}

// 파티클 생성
createParticles(x, y, color, count) {
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = `${x * 50 + 25}px`;
        particle.style.top = `${y * 50 + 25}px`;
        particle.style.background = color;
        particle.style.setProperty('--dx', `${(Math.random() - 0.5) * 100}px`);
        particle.style.setProperty('--dy', `${(Math.random() - 0.5) * 100}px`);
        
        document.getElementById('light-effects').appendChild(particle);
        
        setTimeout(() => particle.remove(), 1000);
    }
}
```

### 2. ↩️ Undo/Redo 시스템 구현

#### 2.1 히스토리 관리
```javascript
// frontend/js/history.js (새 파일)
class HistoryManager {
    constructor(maxHistory = 50) {
        this.history = [];
        this.currentIndex = -1;
        this.maxHistory = maxHistory;
    }
    
    addAction(action) {
        // 현재 위치 이후의 히스토리 제거
        this.history = this.history.slice(0, this.currentIndex + 1);
        
        // 새 액션 추가
        this.history.push({
            ...action,
            timestamp: Date.now()
        });
        
        // 최대 크기 유지
        if (this.history.length > this.maxHistory) {
            this.history.shift();
        } else {
            this.currentIndex++;
        }
        
        this.updateUI();
    }
    
    undo() {
        if (this.canUndo()) {
            const action = this.history[this.currentIndex];
            this.currentIndex--;
            this.updateUI();
            return this.reverseAction(action);
        }
        return null;
    }
    
    redo() {
        if (this.canRedo()) {
            this.currentIndex++;
            const action = this.history[this.currentIndex];
            this.updateUI();
            return action;
        }
        return null;
    }
    
    canUndo() {
        return this.currentIndex >= 0;
    }
    
    canRedo() {
        return this.currentIndex < this.history.length - 1;
    }
    
    reverseAction(action) {
        switch(action.type) {
            case 'place':
                return { type: 'remove', x: action.x, y: action.y };
            case 'remove':
                return { type: 'place', x: action.x, y: action.y, piece: action.piece };
            case 'rotate':
                return { type: 'rotate', x: action.x, y: action.y, direction: -action.direction };
            default:
                return null;
        }
    }
    
    updateUI() {
        const undoBtn = document.getElementById('undo-btn');
        const redoBtn = document.getElementById('redo-btn');
        const historyCount = document.getElementById('history-count');
        
        undoBtn.disabled = !this.canUndo();
        redoBtn.disabled = !this.canRedo();
        
        if (historyCount) {
            historyCount.textContent = `${this.currentIndex + 1}/${this.history.length}`;
        }
        
        // 히스토리 타임라인 업데이트
        this.updateTimeline();
    }
    
    updateTimeline() {
        const timeline = document.getElementById('history-timeline');
        if (!timeline) return;
        
        timeline.innerHTML = '';
        
        this.history.forEach((action, index) => {
            const dot = document.createElement('div');
            dot.className = 'timeline-dot';
            
            if (index <= this.currentIndex) {
                dot.classList.add('active');
            }
            
            if (index === this.currentIndex) {
                dot.classList.add('current');
            }
            
            dot.title = `${action.type} at (${action.x}, ${action.y})`;
            dot.onclick = () => this.jumpTo(index);
            
            timeline.appendChild(dot);
        });
    }
    
    jumpTo(index) {
        if (index < 0 || index >= this.history.length) return;
        
        const steps = index - this.currentIndex;
        
        if (steps > 0) {
            for (let i = 0; i < steps; i++) {
                this.redo();
            }
        } else {
            for (let i = 0; i < Math.abs(steps); i++) {
                this.undo();
            }
        }
    }
}
```

#### 2.2 UI 컴포넌트
```html
<!-- frontend/index.html에 추가 -->
<div class="history-controls">
    <button id="undo-btn" class="history-btn" title="실행 취소 (Ctrl+Z)">
        <svg viewBox="0 0 24 24" width="20" height="20">
            <path d="M12.5 8c-2.65 0-5.05.99-6.9 2.6L2 7v9h9l-3.62-3.62c1.39-1.16 3.16-1.88 5.12-1.88 3.54 0 6.55 2.31 7.6 5.5l2.37-.78C21.08 11.03 17.15 8 12.5 8z"/>
        </svg>
        <span>되돌리기</span>
    </button>
    
    <div id="history-timeline" class="history-timeline"></div>
    
    <button id="redo-btn" class="history-btn" title="다시 실행 (Ctrl+Y)">
        <svg viewBox="0 0 24 24" width="20" height="20">
            <path d="M18.4 10.6C16.55 8.99 14.15 8 11.5 8c-4.65 0-8.58 3.03-9.96 7.22L3.9 16c1.05-3.19 4.05-5.5 7.6-5.5 1.95 0 3.73.72 5.12 1.88L13 16h9V7l-3.6 3.6z"/>
        </svg>
        <span>다시하기</span>
    </button>
    
    <span id="history-count" class="history-count">0/0</span>
</div>
```

```css
/* 히스토리 컨트롤 스타일 */
.history-controls {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    margin: 10px 0;
}

.history-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 6px;
    color: white;
    cursor: pointer;
    transition: all 0.2s;
}

.history-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
}

.history-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.history-timeline {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 0 10px;
    max-width: 300px;
    overflow-x: auto;
}

.timeline-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    cursor: pointer;
    transition: all 0.2s;
}

.timeline-dot.active {
    background: rgba(102, 126, 234, 0.6);
}

.timeline-dot.current {
    width: 12px;
    height: 12px;
    background: #667eea;
    box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
}

.timeline-dot:hover {
    transform: scale(1.5);
}
```

### 3. 🎓 온보딩 튜토리얼

#### 3.1 튜토리얼 매니저
```javascript
// frontend/js/tutorial.js (새 파일)
class TutorialManager {
    constructor() {
        this.steps = [
            {
                title: "Mirror Maze에 오신 것을 환영합니다!",
                content: "빛과 거울을 이용한 퍼즐 게임입니다.",
                target: null,
                action: null
            },
            {
                title: "빛의 원리",
                content: "빛은 직진하다가 거울을 만나면 반사됩니다.",
                target: '.emitter',
                highlight: true,
                animation: 'showLightPath'
            },
            {
                title: "도구 선택",
                content: "왼쪽 패널에서 거울을 선택해보세요.",
                target: '[data-tool="mirror_left"]',
                highlight: true,
                waitForAction: 'tool-select'
            },
            {
                title: "거울 배치",
                content: "게임 보드의 하이라이트된 위치를 클릭하세요.",
                target: '#game-canvas',
                highlightCell: {x: 4, y: 4},
                waitForAction: 'place-piece'
            },
            {
                title: "목표 달성",
                content: "빛이 목표 지점에 도달하면 레벨 완료!",
                target: '.target',
                highlight: true
            },
            {
                title: "준비 완료!",
                content: "이제 첫 번째 레벨에 도전해보세요!",
                action: 'start-game'
            }
        ];
        
        this.currentStep = 0;
        this.overlay = null;
        this.isActive = false;
    }
    
    start() {
        // 첫 방문자 체크
        if (localStorage.getItem('tutorial-completed')) {
            const showAgain = confirm('튜토리얼을 다시 보시겠습니까?');
            if (!showAgain) return;
        }
        
        this.isActive = true;
        this.currentStep = 0;
        this.createOverlay();
        this.showStep(0);
    }
    
    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'tutorial-overlay';
        this.overlay.innerHTML = `
            <div class="tutorial-backdrop"></div>
            <div class="tutorial-spotlight"></div>
            <div class="tutorial-card">
                <div class="tutorial-header">
                    <h3 class="tutorial-title"></h3>
                    <button class="tutorial-close" onclick="tutorial.skip()">×</button>
                </div>
                <div class="tutorial-content"></div>
                <div class="tutorial-footer">
                    <div class="tutorial-progress">
                        <div class="progress-bar">
                            <div class="progress-fill"></div>
                        </div>
                        <span class="step-counter">1/6</span>
                    </div>
                    <div class="tutorial-actions">
                        <button class="btn-skip" onclick="tutorial.skip()">건너뛰기</button>
                        <button class="btn-prev" onclick="tutorial.prevStep()">이전</button>
                        <button class="btn-next" onclick="tutorial.nextStep()">다음</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.overlay);
    }
    
    showStep(index) {
        if (index < 0 || index >= this.steps.length) return;
        
        const step = this.steps[index];
        this.currentStep = index;
        
        // 카드 내용 업데이트
        const card = this.overlay.querySelector('.tutorial-card');
        card.querySelector('.tutorial-title').textContent = step.title;
        card.querySelector('.tutorial-content').textContent = step.content;
        
        // 진행 상황 업데이트
        const progress = (index + 1) / this.steps.length * 100;
        card.querySelector('.progress-fill').style.width = `${progress}%`;
        card.querySelector('.step-counter').textContent = `${index + 1}/${this.steps.length}`;
        
        // 버튼 상태 업데이트
        card.querySelector('.btn-prev').disabled = index === 0;
        card.querySelector('.btn-next').disabled = index === this.steps.length - 1;
        
        // 타겟 하이라이트
        if (step.target) {
            this.highlightElement(step.target);
        } else {
            this.clearHighlight();
        }
        
        // 셀 하이라이트
        if (step.highlightCell) {
            this.highlightCell(step.highlightCell.x, step.highlightCell.y);
        }
        
        // 애니메이션 실행
        if (step.animation) {
            this.playAnimation(step.animation);
        }
        
        // 액션 대기
        if (step.waitForAction) {
            this.waitForAction(step.waitForAction);
        }
        
        // 자동 액션
        if (step.action) {
            this.executeAction(step.action);
        }
    }
    
    highlightElement(selector) {
        const element = document.querySelector(selector);
        if (!element) return;
        
        const rect = element.getBoundingClientRect();
        const spotlight = this.overlay.querySelector('.tutorial-spotlight');
        
        spotlight.style.left = `${rect.left - 10}px`;
        spotlight.style.top = `${rect.top - 10}px`;
        spotlight.style.width = `${rect.width + 20}px`;
        spotlight.style.height = `${rect.height + 20}px`;
        spotlight.style.display = 'block';
        
        // 화살표 추가
        this.addArrow(rect);
    }
    
    addArrow(targetRect) {
        const arrow = document.createElement('div');
        arrow.className = 'tutorial-arrow';
        arrow.innerHTML = '👆';
        arrow.style.left = `${targetRect.left + targetRect.width / 2 - 20}px`;
        arrow.style.top = `${targetRect.bottom + 10}px`;
        
        this.overlay.appendChild(arrow);
    }
    
    clearHighlight() {
        const spotlight = this.overlay.querySelector('.tutorial-spotlight');
        spotlight.style.display = 'none';
        
        // 화살표 제거
        const arrows = this.overlay.querySelectorAll('.tutorial-arrow');
        arrows.forEach(arrow => arrow.remove());
    }
    
    highlightCell(x, y) {
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        
        // 셀 하이라이트
        ctx.strokeStyle = '#10B981';
        ctx.lineWidth = 3;
        ctx.strokeRect(x * 50, y * 50, 50, 50);
        
        // 깜빡임 효과
        let alpha = 0;
        const blink = setInterval(() => {
            alpha = alpha === 0 ? 0.3 : 0;
            ctx.fillStyle = `rgba(16, 185, 129, ${alpha})`;
            ctx.fillRect(x * 50, y * 50, 50, 50);
        }, 500);
        
        setTimeout(() => clearInterval(blink), 3000);
    }
    
    waitForAction(actionType) {
        // 이벤트 리스너 추가
        const handler = (event) => {
            if (event.detail && event.detail.action === actionType) {
                document.removeEventListener('tutorial-action', handler);
                this.nextStep();
            }
        };
        
        document.addEventListener('tutorial-action', handler);
    }
    
    executeAction(action) {
        switch(action) {
            case 'start-game':
                setTimeout(() => {
                    this.complete();
                    game.startLevel(1);
                }, 1000);
                break;
        }
    }
    
    playAnimation(animationType) {
        switch(animationType) {
            case 'showLightPath':
                // 빛 경로 애니메이션
                this.animateLightPath();
                break;
        }
    }
    
    animateLightPath() {
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        
        let progress = 0;
        const animate = () => {
            if (progress > 100) return;
            
            ctx.strokeStyle = '#FFD700';
            ctx.lineWidth = 3;
            ctx.setLineDash([5, 5]);
            ctx.lineDashOffset = -progress;
            
            ctx.beginPath();
            ctx.moveTo(50, 225);
            ctx.lineTo(250, 225);
            ctx.stroke();
            
            progress += 2;
            requestAnimationFrame(animate);
        };
        
        animate();
    }
    
    nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.showStep(this.currentStep + 1);
        } else {
            this.complete();
        }
    }
    
    prevStep() {
        if (this.currentStep > 0) {
            this.showStep(this.currentStep - 1);
        }
    }
    
    skip() {
        const confirm = window.confirm('튜토리얼을 건너뛰시겠습니까?');
        if (confirm) {
            this.complete();
        }
    }
    
    complete() {
        localStorage.setItem('tutorial-completed', 'true');
        this.isActive = false;
        
        // 완료 애니메이션
        this.overlay.style.animation = 'fadeOut 0.5s ease-out';
        
        setTimeout(() => {
            this.overlay.remove();
            this.overlay = null;
        }, 500);
        
        // 완료 메시지
        this.showCompletionMessage();
    }
    
    showCompletionMessage() {
        const message = document.createElement('div');
        message.className = 'completion-message';
        message.innerHTML = `
            <div class="message-content">
                <h2>🎉 튜토리얼 완료!</h2>
                <p>이제 게임을 시작할 준비가 되었습니다!</p>
                <button onclick="this.parentElement.parentElement.remove()">시작하기</button>
            </div>
        `;
        
        document.body.appendChild(message);
        
        setTimeout(() => {
            message.style.animation = 'fadeOut 0.5s ease-out';
            setTimeout(() => message.remove(), 500);
        }, 3000);
    }
}

// 튜토리얼 인스턴스 생성
const tutorial = new TutorialManager();
```

#### 3.2 튜토리얼 스타일
```css
/* 튜토리얼 오버레이 */
.tutorial-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10000;
    animation: fadeIn 0.3s ease-out;
}

.tutorial-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
}

.tutorial-spotlight {
    position: absolute;
    border: 3px solid #10B981;
    border-radius: 8px;
    box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.7);
    z-index: 10001;
    display: none;
    animation: spotlightPulse 2s infinite;
}

@keyframes spotlightPulse {
    0%, 100% { box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.7); }
    50% { box-shadow: 0 0 20px #10B981, 0 0 0 9999px rgba(0, 0, 0, 0.7); }
}

.tutorial-card {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    border-radius: 12px;
    padding: 20px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    z-index: 10002;
    animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
    from {
        transform: translateX(-50%) translateY(100px);
        opacity: 0;
    }
    to {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }
}

.tutorial-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.tutorial-title {
    font-size: 1.2em;
    font-weight: bold;
    color: #333;
    margin: 0;
}

.tutorial-close {
    background: none;
    border: none;
    font-size: 24px;
    color: #999;
    cursor: pointer;
    padding: 0;
    width: 30px;
    height: 30px;
}

.tutorial-content {
    color: #666;
    line-height: 1.5;
    margin-bottom: 20px;
}

.tutorial-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.tutorial-progress {
    display: flex;
    align-items: center;
    gap: 10px;
}

.progress-bar {
    width: 100px;
    height: 4px;
    background: #e0e0e0;
    border-radius: 2px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: #667eea;
    transition: width 0.3s ease;
}

.step-counter {
    font-size: 0.9em;
    color: #999;
}

.tutorial-actions {
    display: flex;
    gap: 10px;
}

.tutorial-actions button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9em;
    transition: all 0.2s;
}

.btn-skip {
    background: transparent;
    color: #999;
}

.btn-prev {
    background: #f0f0f0;
    color: #666;
}

.btn-next {
    background: #667eea;
    color: white;
}

.btn-next:hover {
    background: #5a67d8;
}

.tutorial-arrow {
    position: absolute;
    font-size: 30px;
    animation: bounce 1s infinite;
    z-index: 10003;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.completion-message {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    z-index: 10004;
    animation: scaleIn 0.3s ease-out;
}

@keyframes scaleIn {
    from {
        transform: translate(-50%, -50%) scale(0.8);
        opacity: 0;
    }
    to {
        transform: translate(-50%, -50%) scale(1);
        opacity: 1;
    }
}
```

### 4. 📱 모바일 최적화

#### 4.1 터치 이벤트 처리
```javascript
// frontend/js/touch-handler.js (새 파일)
class TouchHandler {
    constructor(canvas) {
        this.canvas = canvas;
        this.touchStartPos = null;
        this.isDragging = false;
        this.selectedPiece = null;
        
        this.init();
    }
    
    init() {
        // 터치 이벤트
        this.canvas.addEventListener('touchstart', this.handleTouchStart.bind(this));
        this.canvas.addEventListener('touchmove', this.handleTouchMove.bind(this));
        this.canvas.addEventListener('touchend', this.handleTouchEnd.bind(this));
        
        // 제스처 방지
        this.canvas.addEventListener('gesturestart', (e) => e.preventDefault());
        
        // 더블 탭 줌 방지
        let lastTouchEnd = 0;
        this.canvas.addEventListener('touchend', (e) => {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        });
    }
    
    handleTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const rect = this.canvas.getBoundingClientRect();
        
        this.touchStartPos = {
            x: touch.clientX - rect.left,
            y: touch.clientY - rect.top,
            time: Date.now()
        };
        
        // 롱프레스 감지
        this.longPressTimer = setTimeout(() => {
            this.handleLongPress(this.touchStartPos);
        }, 500);
    }
    
    handleTouchMove(e) {
        e.preventDefault();
        
        if (!this.touchStartPos) return;
        
        const touch = e.touches[0];
        const rect = this.canvas.getBoundingClientRect();
        const currentPos = {
            x: touch.clientX - rect.left,
            y: touch.clientY - rect.top
        };
        
        const dx = currentPos.x - this.touchStartPos.x;
        const dy = currentPos.y - this.touchStartPos.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // 드래그 감지
        if (distance > 10) {
            clearTimeout(this.longPressTimer);
            this.isDragging = true;
            
            if (this.selectedPiece) {
                this.dragPiece(currentPos);
            }
        }
    }
    
    handleTouchEnd(e) {
        e.preventDefault();
        clearTimeout(this.longPressTimer);
        
        if (!this.touchStartPos) return;
        
        const touch = e.changedTouches[0];
        const rect = this.canvas.getBoundingClientRect();
        const endPos = {
            x: touch.clientX - rect.left,
            y: touch.clientY - rect.top
        };
        
        const timeDiff = Date.now() - this.touchStartPos.time;
        const dx = endPos.x - this.touchStartPos.x;
        const dy = endPos.y - this.touchStartPos.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 10 && timeDiff < 200) {
            // 탭
            this.handleTap(endPos);
        } else if (this.isDragging && this.selectedPiece) {
            // 드롭
            this.dropPiece(endPos);
        }
        
        this.touchStartPos = null;
        this.isDragging = false;
        this.selectedPiece = null;
    }
    
    handleTap(pos) {
        const x = Math.floor(pos.x / 50);
        const y = Math.floor(pos.y / 50);
        
        // 게임 액션 실행
        game.handleCanvasClick({
            clientX: pos.x,
            clientY: pos.y
        });
        
        // 햅틱 피드백
        if ('vibrate' in navigator) {
            navigator.vibrate(10);
        }
    }
    
    handleLongPress(pos) {
        const x = Math.floor(pos.x / 50);
        const y = Math.floor(pos.y / 50);
        
        // 도구 정보 표시
        this.showPieceInfo(x, y);
        
        // 강한 햅틱 피드백
        if ('vibrate' in navigator) {
            navigator.vibrate([50, 50, 50]);
        }
    }
    
    dragPiece(pos) {
        // 드래그 중인 조각 표시
        const ctx = this.canvas.getContext('2d');
        
        // 임시 캔버스에 그리기
        ctx.save();
        ctx.globalAlpha = 0.7;
        // 드래그 중인 조각 그리기
        this.drawDraggedPiece(pos.x, pos.y);
        ctx.restore();
    }
    
    dropPiece(pos) {
        const x = Math.floor(pos.x / 50);
        const y = Math.floor(pos.y / 50);
        
        // 조각 배치
        if (this.selectedPiece) {
            game.placePiece(x, y, this.selectedPiece);
        }
    }
    
    showPieceInfo(x, y) {
        const piece = game.getPieceAt(x, y);
        if (!piece) return;
        
        // 정보 팝업 표시
        const popup = document.createElement('div');
        popup.className = 'piece-info-popup';
        popup.innerHTML = `
            <h4>${piece.type}</h4>
            <p>${piece.description}</p>
            <button onclick="this.parentElement.remove()">닫기</button>
        `;
        
        popup.style.left = `${x * 50}px`;
        popup.style.top = `${y * 50}px`;
        
        document.getElementById('game-screen').appendChild(popup);
        
        setTimeout(() => popup.remove(), 3000);
    }
}
```

#### 4.2 반응형 레이아웃
```css
/* 모바일 최적화 스타일 */
@media (max-width: 768px) {
    /* 전체 화면 게임 */
    #app {
        padding: 0;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    .game-header {
        padding: 10px;
        border-radius: 0;
        margin-bottom: 0;
    }
    
    .game-container {
        flex: 1;
        overflow: hidden;
    }
    
    /* 하단 도구 패널 */
    .tool-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: rgba(0, 0, 0, 0.9);
        border-top: 2px solid rgba(255, 255, 255, 0.2);
        display: flex;
        overflow-x: auto;
        padding: 10px;
        gap: 10px;
        z-index: 1000;
    }
    
    .tool {
        min-width: 60px;
        height: 60px;
        flex-shrink: 0;
    }
    
    /* 게임 보드 크기 조정 */
    #game-canvas {
        width: calc(100vw - 20px);
        height: calc(100vw - 20px);
        max-width: 500px;
        max-height: 500px;
        margin: 10px auto;
    }
    
    /* 정보 패널 숨기기/표시 토글 */
    .info-panel {
        position: fixed;
        right: -250px;
        top: 60px;
        bottom: 90px;
        width: 250px;
        transition: right 0.3s ease;
        z-index: 999;
    }
    
    .info-panel.open {
        right: 0;
    }
    
    /* 정보 패널 토글 버튼 */
    .info-toggle {
        position: fixed;
        right: 10px;
        top: 70px;
        width: 40px;
        height: 40px;
        background: rgba(102, 126, 234, 0.9);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        z-index: 1001;
    }
    
    /* 터치 친화적 버튼 */
    .btn {
        min-height: 44px;
        font-size: 14px;
    }
    
    /* 모달 최적화 */
    .modal-content {
        width: 90%;
        padding: 20px;
    }
    
    /* 승리 화면 */
    .victory-buttons {
        flex-direction: column;
        width: 100%;
    }
    
    .victory-buttons .btn {
        width: 100%;
        margin: 5px 0;
    }
}

/* 태블릿 최적화 */
@media (min-width: 768px) and (max-width: 1024px) {
    .game-area {
        grid-template-columns: 120px 1fr 200px;
        gap: 15px;
    }
    
    .tool {
        width: 100px;
        height: 50px;
    }
    
    #game-canvas {
        width: 450px;
        height: 450px;
    }
}

/* 가로 모드 최적화 */
@media (orientation: landscape) and (max-height: 600px) {
    .game-header {
        padding: 5px 10px;
    }
    
    .game-header h1 {
        font-size: 1.2em;
    }
    
    .tool-panel {
        height: 60px;
    }
    
    .tool {
        height: 40px;
        min-width: 50px;
    }
    
    #game-canvas {
        height: calc(100vh - 140px);
        width: calc(100vh - 140px);
    }
}
```

### 5. 🎯 구현 체크리스트

#### Phase 1 (즉시 구현)
- [ ] 도구 선택 피드백 강화
- [ ] 호버 상태 개선
- [ ] 배치 애니메이션
- [ ] 기본 Undo/Redo
- [ ] 키보드 단축키

#### Phase 2 (1주일 내)
- [ ] 온보딩 튜토리얼
- [ ] 히스토리 타임라인
- [ ] 모바일 터치 지원
- [ ] 반응형 레이아웃
- [ ] 사운드 효과

#### Phase 3 (2주일 내)
- [ ] 적응형 힌트 시스템
- [ ] 진행 상황 대시보드
- [ ] 도전 과제
- [ ] 개인화 설정
- [ ] 접근성 기능

---

*이 가이드를 참고하여 단계적으로 UX를 개선해 나가세요!*