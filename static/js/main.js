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
    
    // Login button functionaliteit - voor later gebruik
    const loginButton = document.querySelector('.google-login-btn');
    if (loginButton) {
        loginButton.addEventListener('click', function(e) {
            console.log('Login button clicked');
            // OAuth login zal later worden geïmplementeerd
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
