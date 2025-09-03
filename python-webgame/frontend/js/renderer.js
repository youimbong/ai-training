/**
 * Canvas Renderer for Mirror Maze
 */

class GameRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.cellSize = 50;
        this.gridSize = 10;
        this.gameState = null;
        this.lightPaths = [];
        this.hoverX = -1;
        this.hoverY = -1;
        this.animations = [];
    }
    
    updateGameState(gameState, lightPaths) {
        this.gameState = gameState;
        this.lightPaths = lightPaths || [];
    }
    
    setHoverPosition(x, y) {
        this.hoverX = x;
        this.hoverY = y;
    }
    
    render() {
        if (!this.gameState) return;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw grid
        this.drawGrid();
        
        // Draw walls
        this.drawWalls();
        
        // Draw placed pieces
        this.drawPieces();
        
        // Draw emitters
        this.drawEmitters();
        
        // Draw targets
        this.drawTargets();
        
        // Draw light paths
        this.drawLightPaths();
        
        // Draw hover effect
        this.drawHover();
        
        // Update animations
        this.updateAnimations();
    }
    
    drawGrid() {
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.lineWidth = 1;
        
        for (let i = 0; i <= this.gridSize; i++) {
            // Vertical lines
            this.ctx.beginPath();
            this.ctx.moveTo(i * this.cellSize, 0);
            this.ctx.lineTo(i * this.cellSize, this.gridSize * this.cellSize);
            this.ctx.stroke();
            
            // Horizontal lines
            this.ctx.beginPath();
            this.ctx.moveTo(0, i * this.cellSize);
            this.ctx.lineTo(this.gridSize * this.cellSize, i * this.cellSize);
            this.ctx.stroke();
        }
    }
    
    drawWalls() {
        if (!this.gameState.grid) return;
        
        this.ctx.fillStyle = '#333';
        
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                if (this.gameState.grid[y][x] === 'wall') {
                    this.drawCell(x, y, '#333');
                }
            }
        }
    }
    
    drawPieces() {
        if (!this.gameState.grid) return;
        
        for (let y = 0; y < this.gridSize; y++) {
            for (let x = 0; x < this.gridSize; x++) {
                const cell = this.gameState.grid[y][x];
                
                if (cell === 'mirror_left') {
                    this.drawMirror(x, y, 'left');
                } else if (cell === 'mirror_right') {
                    this.drawMirror(x, y, 'right');
                } else if (cell === 'splitter') {
                    this.drawSplitter(x, y);
                } else if (cell === 'prism') {
                    this.drawPrism(x, y);
                } else if (cell.startsWith('filter_')) {
                    const color = cell.split('_')[1];
                    this.drawFilter(x, y, color);
                }
            }
        }
    }
    
    drawEmitters() {
        if (!this.gameState.emitters) return;
        
        this.gameState.emitters.forEach(emitter => {
            const cx = emitter.x * this.cellSize + this.cellSize / 2;
            const cy = emitter.y * this.cellSize + this.cellSize / 2;
            
            // Draw emitter body
            this.ctx.fillStyle = '#666';
            this.ctx.fillRect(
                emitter.x * this.cellSize + 10,
                emitter.y * this.cellSize + 10,
                this.cellSize - 20,
                this.cellSize - 20
            );
            
            // Draw light source
            const gradient = this.ctx.createRadialGradient(cx, cy, 0, cx, cy, 15);
            gradient.addColorStop(0, this.getColorValue(emitter.color));
            gradient.addColorStop(1, 'transparent');
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(cx, cy, 15, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Draw direction indicator
            this.ctx.strokeStyle = this.getColorValue(emitter.color);
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            
            const dir = this.getDirectionVector(emitter.direction);
            this.ctx.moveTo(cx, cy);
            this.ctx.lineTo(cx + dir.x * 20, cy + dir.y * 20);
            this.ctx.stroke();
            
            // Arrow head
            this.drawArrowHead(cx + dir.x * 20, cy + dir.y * 20, dir);
        });
    }
    
    drawTargets() {
        if (!this.gameState.targets) return;
        
        this.gameState.targets.forEach(target => {
            const cx = target.x * this.cellSize + this.cellSize / 2;
            const cy = target.y * this.cellSize + this.cellSize / 2;
            
            // Draw target circle
            this.ctx.strokeStyle = this.getColorValue(target.required_color);
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            this.ctx.arc(cx, cy, 20, 0, Math.PI * 2);
            this.ctx.stroke();
            
            // Draw inner circle
            if (target.is_hit) {
                this.ctx.fillStyle = this.getColorValue(target.required_color);
                this.ctx.globalAlpha = 0.5;
                this.ctx.beginPath();
                this.ctx.arc(cx, cy, 15, 0, Math.PI * 2);
                this.ctx.fill();
                this.ctx.globalAlpha = 1;
                
                // Draw checkmark
                this.ctx.strokeStyle = '#fff';
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.moveTo(cx - 8, cy);
                this.ctx.lineTo(cx - 2, cy + 6);
                this.ctx.lineTo(cx + 8, cy - 6);
                this.ctx.stroke();
            } else {
                // Draw X for unhit targets
                this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.arc(cx, cy, 10, 0, Math.PI * 2);
                this.ctx.stroke();
            }
        });
    }
    
    drawLightPaths() {
        if (!this.lightPaths) return;
        
        this.lightPaths.forEach(pathData => {
            const color = this.getColorValue(pathData.color);
            
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = 4;
            this.ctx.globalAlpha = 0.8;
            this.ctx.shadowBlur = 10;
            this.ctx.shadowColor = color;
            
            this.ctx.beginPath();
            pathData.path.forEach((point, index) => {
                const x = point[0] * this.cellSize + this.cellSize / 2;
                const y = point[1] * this.cellSize + this.cellSize / 2;
                
                if (index === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
            });
            this.ctx.stroke();
            
            this.ctx.shadowBlur = 0;
            this.ctx.globalAlpha = 1;
        });
    }
    
    drawMirror(x, y, type) {
        const cx = x * this.cellSize + this.cellSize / 2;
        const cy = y * this.cellSize + this.cellSize / 2;
        
        // Draw mirror base
        this.ctx.fillStyle = 'rgba(200, 200, 200, 0.3)';
        this.ctx.fillRect(
            x * this.cellSize + 5,
            y * this.cellSize + 5,
            this.cellSize - 10,
            this.cellSize - 10
        );
        
        // Draw mirror line
        this.ctx.strokeStyle = '#fff';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        
        if (type === 'left') { // \ mirror
            this.ctx.moveTo(x * this.cellSize + 10, y * this.cellSize + 10);
            this.ctx.lineTo(x * this.cellSize + 40, y * this.cellSize + 40);
        } else { // / mirror
            this.ctx.moveTo(x * this.cellSize + 40, y * this.cellSize + 10);
            this.ctx.lineTo(x * this.cellSize + 10, y * this.cellSize + 40);
        }
        this.ctx.stroke();
        
        // Add reflection effect
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    }
    
    drawSplitter(x, y) {
        const cx = x * this.cellSize + this.cellSize / 2;
        const cy = y * this.cellSize + this.cellSize / 2;
        
        // Draw splitter base
        this.ctx.fillStyle = 'rgba(100, 100, 200, 0.3)';
        this.ctx.fillRect(
            x * this.cellSize + 10,
            y * this.cellSize + 10,
            this.cellSize - 20,
            this.cellSize - 20
        );
        
        // Draw cross
        this.ctx.strokeStyle = '#66f';
        this.ctx.lineWidth = 3;
        
        this.ctx.beginPath();
        this.ctx.moveTo(cx, y * this.cellSize + 15);
        this.ctx.lineTo(cx, y * this.cellSize + 35);
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(x * this.cellSize + 15, cy);
        this.ctx.lineTo(x * this.cellSize + 35, cy);
        this.ctx.stroke();
    }
    
    drawPrism(x, y) {
        const cx = x * this.cellSize + this.cellSize / 2;
        const cy = y * this.cellSize + this.cellSize / 2;
        
        // Draw prism triangle
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
        this.ctx.strokeStyle = '#fff';
        this.ctx.lineWidth = 2;
        
        this.ctx.beginPath();
        this.ctx.moveTo(cx, y * this.cellSize + 15);
        this.ctx.lineTo(x * this.cellSize + 35, y * this.cellSize + 35);
        this.ctx.lineTo(x * this.cellSize + 15, y * this.cellSize + 35);
        this.ctx.closePath();
        this.ctx.fill();
        this.ctx.stroke();
        
        // Add rainbow effect
        const gradient = this.ctx.createLinearGradient(
            x * this.cellSize + 15,
            cy,
            x * this.cellSize + 35,
            cy
        );
        gradient.addColorStop(0, 'rgba(255, 0, 0, 0.3)');
        gradient.addColorStop(0.5, 'rgba(0, 255, 0, 0.3)');
        gradient.addColorStop(1, 'rgba(0, 0, 255, 0.3)');
        
        this.ctx.fillStyle = gradient;
        this.ctx.fill();
    }
    
    drawFilter(x, y, color) {
        const cx = x * this.cellSize + this.cellSize / 2;
        const cy = y * this.cellSize + this.cellSize / 2;
        
        const colorValue = this.getColorValue(color.toUpperCase());
        
        // Draw filter circle
        this.ctx.fillStyle = colorValue + '33'; // Add transparency
        this.ctx.strokeStyle = colorValue;
        this.ctx.lineWidth = 2;
        
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, 18, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.stroke();
    }
    
    drawHover() {
        if (this.hoverX >= 0 && this.hoverY >= 0 && 
            this.hoverX < this.gridSize && this.hoverY < this.gridSize) {
            
            this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(
                this.hoverX * this.cellSize,
                this.hoverY * this.cellSize,
                this.cellSize,
                this.cellSize
            );
        }
    }
    
    drawCell(x, y, color) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(
            x * this.cellSize,
            y * this.cellSize,
            this.cellSize,
            this.cellSize
        );
    }
    
    drawArrowHead(x, y, dir) {
        const size = 8;
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(x - dir.x * size - dir.y * size/2, y - dir.y * size + dir.x * size/2);
        this.ctx.lineTo(x - dir.x * size + dir.y * size/2, y - dir.y * size - dir.x * size/2);
        this.ctx.closePath();
        this.ctx.fill();
    }
    
    getColorValue(colorName) {
        const colors = {
            'WHITE': '#ffffff',
            'RED': '#ff0000',
            'GREEN': '#00ff00',
            'BLUE': '#0000ff',
            'YELLOW': '#ffff00',
            'CYAN': '#00ffff',
            'MAGENTA': '#ff00ff',
            'white': '#ffffff',
            'red': '#ff0000',
            'green': '#00ff00',
            'blue': '#0000ff',
            'yellow': '#ffff00',
            'cyan': '#00ffff',
            'magenta': '#ff00ff'
        };
        return colors[colorName] || '#ffffff';
    }
    
    getDirectionVector(direction) {
        const directions = {
            'UP': { x: 0, y: -1 },
            'DOWN': { x: 0, y: 1 },
            'LEFT': { x: -1, y: 0 },
            'RIGHT': { x: 1, y: 0 }
        };
        return directions[direction] || { x: 0, y: 0 };
    }
    
    updateAnimations() {
        // Particle effects and other animations
        this.animations = this.animations.filter(anim => {
            anim.update();
            anim.draw(this.ctx);
            return !anim.finished;
        });
    }
    
    addParticleEffect(x, y, color) {
        // Add particle explosion effect
        for (let i = 0; i < 20; i++) {
            this.animations.push(new Particle(x, y, color));
        }
    }
}

// Particle class for effects
class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 4;
        this.vy = (Math.random() - 0.5) * 4;
        this.color = color;
        this.life = 1.0;
        this.finished = false;
    }
    
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life -= 0.02;
        if (this.life <= 0) {
            this.finished = true;
        }
    }
    
    draw(ctx) {
        if (this.finished) return;
        
        ctx.globalAlpha = this.life;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x - 2, this.y - 2, 4, 4);
        ctx.globalAlpha = 1;
    }
}

// Create renderer instance
window.renderer = new GameRenderer('game-canvas');