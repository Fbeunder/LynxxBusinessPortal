/**
 * Lynxx Business Portal - Main JavaScript
 * 
 * Dit bestand bevat de algemene JavaScript-functionaliteit voor de Lynxx Business Portal.
 */

// Wacht tot DOM volledig is geladen
document.addEventListener('DOMContentLoaded', function() {
    console.log('Lynxx Business Portal loaded');
    
    // Event listeners voor app tegels
    initializeAppTiles();
    
    // Flash messages automatisch verbergen na 5 seconden
    handleFlashMessages();
    
    // Logout bevestiging
    setupLogoutConfirmation();
});

/**
 * Initialiseert functionaliteit voor app tegels
 */
function initializeAppTiles() {
    const appTiles = document.querySelectorAll('.app-tile');
    if (appTiles && appTiles.length > 0) {
        console.log(`Gevonden app tegels: ${appTiles.length}`);
        
        appTiles.forEach(tile => {
            // Voeg hover effect toe
            tile.addEventListener('mouseenter', function() {
                this.classList.add('hover');
            });
            
            tile.addEventListener('mouseleave', function() {
                this.classList.remove('hover');
            });
            
            // Open links en log gebruik
            tile.addEventListener('click', function(e) {
                const appName = this.querySelector('h3').textContent;
                const appId = this.getAttribute('data-app-id');
                
                console.log(`App geopend: ${appName} (ID: ${appId})`);
                
                // Hier kunnen we later gebruiksstatistieken bijhouden
                // Bijvoorbeeld via een AJAX call naar een /api/track endpoint
                
                // We laten de standaard link navigatie doorgaan
                // omdat we target="_blank" gebruiken in de HTML
            });
        });
    } else {
        console.warn('Geen app tegels gevonden in de DOM');
    }
}

/**
 * Handelt flash messages af (automatisch verbergen)
 */
function handleFlashMessages() {
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
}

/**
 * Configureert logout bevestiging
 */
function setupLogoutConfirmation() {
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            if (!confirm('Weet je zeker dat je wilt uitloggen?')) {
                e.preventDefault();
            }
        });
    }
}

/**
 * Helper functie voor datum en tijd
 * @returns {string} De huidige datum en tijd in een geformatteerde string
 */
function getCurrentDateTime() {
    const now = new Date();
    return now.toLocaleString('nl-NL', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Filtert app tegels op basis van zoekopdracht (voor toekomstige zoekfunctionaliteit)
 * @param {string} query - De zoekopdracht
 */
function filterApps(query) {
    // Deze functie is voorbereid voor toekomstige zoekfunctionaliteit
    const appTiles = document.querySelectorAll('.app-tile');
    const normalizedQuery = query.toLowerCase().trim();
    
    appTiles.forEach(tile => {
        const appName = tile.querySelector('h3').textContent.toLowerCase();
        const appDesc = tile.querySelector('p').textContent.toLowerCase();
        
        if (appName.includes(normalizedQuery) || appDesc.includes(normalizedQuery)) {
            tile.style.display = '';
        } else {
            tile.style.display = 'none';
        }
    });
}
