/**
 * Main entry point for Mirror Maze
 */

document.addEventListener('DOMContentLoaded', async () => {
    // Initialize game
    await game.init();
    
    // Start render loop
    function animate() {
        if (window.renderer) {
            window.renderer.render();
        }
        requestAnimationFrame(animate);
    }
    
    animate();
    
    console.log('🎮 Mirror Maze initialized');
});