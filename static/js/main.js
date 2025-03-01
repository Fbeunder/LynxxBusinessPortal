/**
 * Lynxx Business Portal - Main JavaScript
 * 
 * Dit bestand bevat de algemene JavaScript-functionaliteit voor de Lynxx Business Portal.
 */

// Wacht tot DOM volledig is geladen
document.addEventListener('DOMContentLoaded', function() {
    console.log('Lynxx Business Portal loaded');
    
    // Event listeners voor app tegels - voor later gebruik
    const appTiles = document.querySelectorAll('.app-tile');
    if (appTiles) {
        appTiles.forEach(tile => {
            tile.addEventListener('click', function(e) {
                // Open links in een nieuw tabblad
                // Dit is al ingesteld met target="_blank" in de HTML, dus dit is alleen voor toekomstige functionaliteit
                console.log('App tile clicked:', tile.querySelector('h3').textContent);
            });
        });
    }
    
    // Flash messages automatisch verbergen na 5 seconden
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                message.style.transition = 'opacity 0.5s ease-out';
                setTimeout(() => {
                    message.remove();
                }, 500);
            }, 5000);
        });
    }
    
    // Logout bevestiging
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            if (!confirm('Weet je zeker dat je wilt uitloggen?')) {
                e.preventDefault();
            }
        });
    }
});

/**
 * Helper functie voor datum en tijd - voor later gebruik
 * @returns {string} De huidige datum en tijd in een geformatteerde string
 */
function getCurrentDateTime() {
    const now = new Date();
    return now.toLocaleString();
}