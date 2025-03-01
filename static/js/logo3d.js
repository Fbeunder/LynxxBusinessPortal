/**
 * Lynxx Business Portal - 3D Logo Animation
 * 
 * Dit bestand bevat de Three.js implementatie voor het 3D-roterende Lynxx-logo.
 * Het logo draait langzaam om zijn as in de header van de pagina en reageert op gebruikersinteractie.
 */

// Globale variabelen voor de 3D omgeving
let scene, camera, renderer, logoGroup;
let isMouseDown = false;
let rotationSpeed = { x: 0.003, y: 0.005 };
let autoRotate = true;
let previousMousePosition = { x: 0, y: 0 };
let targetRotation = { x: 0, y: 0 };
let currentRotation = { x: 0, y: 0 };

// Wacht tot DOM volledig is geladen
document.addEventListener('DOMContentLoaded', function() {
    initLogo3D();
});

/**
 * Initialiseert de 3D logo animatie met Three.js
 */
function initLogo3D() {
    // Controleer of het logo container element bestaat
    const container = document.getElementById('logo3d');
    if (!container) return;
    
    // Tooltip voor interactie-hint toevoegen
    const tooltip = document.createElement('div');
    tooltip.className = 'logo-tooltip';
    tooltip.textContent = 'Klik en sleep om te draaien';
    container.appendChild(tooltip);
    
    // Scene, camera en renderer instellen
    scene = new THREE.Scene();
    
    // Camera instellen met goede verhoudingen voor de container
    const aspectRatio = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(60, aspectRatio, 0.1, 1000);
    camera.position.z = 8;
    
    // Renderer instellen met transparante achtergrond en anti-aliasing
    renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true
    });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000, 0); // Transparante achtergrond
    renderer.setPixelRatio(window.devicePixelRatio); // Voor scherpere weergave op high-DPI schermen
    container.appendChild(renderer.domElement);
    
    // Belichting instellen voor betere 3D weergave
    setupLighting();
    
    // Logo model laden
    loadLogoModel();
    
    // Event listeners voor interactie toevoegen
    setupEventListeners(container);
    
    // Animatie-loop starten
    animate();
    
    // Window resize handler
    window.addEventListener('resize', onWindowResize);
}

/**
 * Stelt de belichting in voor de 3D scene
 */
function setupLighting() {
    // Basisverlichting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);
    
    // Hoofdlicht vanaf de voorkant
    const frontLight = new THREE.DirectionalLight(0xffffff, 0.8);
    frontLight.position.set(0, 0, 10);
    scene.add(frontLight);
    
    // Licht vanaf de zijkant voor betere diepteweergave
    const sideLight = new THREE.DirectionalLight(0xffffff, 0.3);
    sideLight.position.set(10, 5, 0);
    scene.add(sideLight);
    
    // Zacht licht van boven
    const topLight = new THREE.DirectionalLight(0xffffff, 0.2);
    topLight.position.set(0, 10, 0);
    scene.add(topLight);
}

/**
 * Laadt het 3D Lynxx logo model
 */
function loadLogoModel() {
    // Gebruik de model generator functie om het logo te creëren
    logoGroup = createLynxxLogoModel({
        depth: 0.3,
        color: '#0099ff',
        letterSpacing: 0.15,
        bevel: true,
        bevelSize: 0.02
    });
    
    // Voeg het logo toe aan de scene
    scene.add(logoGroup);
    
    // Pas de schaal aan zodat het goed in beeld past
    logoGroup.scale.set(0.8, 0.8, 0.8);
    
    // Initiële rotatie om het logo beter zichtbaar te maken
    logoGroup.rotation.x = 0.2;
    logoGroup.rotation.y = 0.4;
    
    // Sla de initiële rotatie op als target en current
    targetRotation.x = logoGroup.rotation.x;
    targetRotation.y = logoGroup.rotation.y;
    currentRotation.x = logoGroup.rotation.x;
    currentRotation.y = logoGroup.rotation.y;
}

/**
 * Zorgt ervoor dat de 3D weergave aangepast wordt als het venster van grootte verandert
 */
function onWindowResize() {
    const container = document.getElementById('logo3d');
    if (!container) return;
    
    const newWidth = container.clientWidth;
    const newHeight = container.clientHeight;
    
    camera.aspect = newWidth / newHeight;
    camera.updateProjectionMatrix();
    
    renderer.setSize(newWidth, newHeight);
}

/**
 * Voegt event listeners toe voor gebruikersinteractie
 * @param {HTMLElement} container Het DOM element dat de 3D weergave bevat
 */
function setupEventListeners(container) {
    // Muisinteractie voor desktop
    container.addEventListener('mousedown', onMouseDown);
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
    
    // Touch interactie voor mobiel
    container.addEventListener('touchstart', onTouchStart);
    document.addEventListener('touchmove', onTouchMove);
    document.addEventListener('touchend', onTouchEnd);
    
    // Wissel tussen automatisch draaien en handmatig draaien bij dubbelklik
    container.addEventListener('dblclick', function() {
        autoRotate = !autoRotate;
        const tooltip = container.querySelector('.logo-tooltip');
        if (tooltip) {
            tooltip.textContent = autoRotate ? 'Klik en sleep om te draaien' : 'Dubbelklik voor automatisch draaien';
        }
    });
}

/**
 * Handler voor het indrukken van de muisknop
 */
function onMouseDown(event) {
    event.preventDefault();
    isMouseDown = true;
    autoRotate = false;
    previousMousePosition = {
        x: event.clientX,
        y: event.clientY
    };
}

/**
 * Handler voor muisbewegingen
 */
function onMouseMove(event) {
    if (!isMouseDown) return;
    
    const deltaMove = {
        x: event.clientX - previousMousePosition.x,
        y: event.clientY - previousMousePosition.y
    };
    
    // Bereken nieuwe doelrotatie gebaseerd op muisbeweging
    targetRotation.y += deltaMove.x * 0.01;
    targetRotation.x += deltaMove.y * 0.01;
    
    // Beperk rotatie om X-as om te voorkomen dat het logo ondersteboven draait
    targetRotation.x = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, targetRotation.x));
    
    previousMousePosition = {
        x: event.clientX,
        y: event.clientY
    };
}

/**
 * Handler voor het loslaten van de muisknop
 */
function onMouseUp() {
    isMouseDown = false;
}

/**
 * Handler voor het aanraken van het scherm (touch start)
 */
function onTouchStart(event) {
    if (event.touches.length === 1) {
        event.preventDefault();
        isMouseDown = true;
        autoRotate = false;
        previousMousePosition = {
            x: event.touches[0].clientX,
            y: event.touches[0].clientY
        };
    }
}

/**
 * Handler voor het bewegen van een vinger over het scherm (touch move)
 */
function onTouchMove(event) {
    if (isMouseDown && event.touches.length === 1) {
        const deltaMove = {
            x: event.touches[0].clientX - previousMousePosition.x,
            y: event.touches[0].clientY - previousMousePosition.y
        };
        
        // Bereken nieuwe doelrotatie gebaseerd op touch beweging
        targetRotation.y += deltaMove.x * 0.01;
        targetRotation.x += deltaMove.y * 0.01;
        
        // Beperk rotatie om X-as
        targetRotation.x = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, targetRotation.x));
        
        previousMousePosition = {
            x: event.touches[0].clientX,
            y: event.touches[0].clientY
        };
    }
}

/**
 * Handler voor het loslaten van het scherm (touch end)
 */
function onTouchEnd() {
    isMouseDown = false;
}

/**
 * Animatie-loop voor het renderen van de 3D scene
 */
function animate() {
    requestAnimationFrame(animate);
    
    if (logoGroup) {
        // Automatische rotatie als ingeschakeld en er geen handmatige interactie is
        if (autoRotate && !isMouseDown) {
            targetRotation.y += rotationSpeed.y;
            targetRotation.x = 0.2 * Math.sin(Date.now() * 0.001) + 0.2;
        }
        
        // Smooth interpolatie naar de doelrotatie
        currentRotation.x += (targetRotation.x - currentRotation.x) * 0.1;
        currentRotation.y += (targetRotation.y - currentRotation.y) * 0.1;
        
        // Pas de huidige rotatie toe op het logo
        logoGroup.rotation.x = currentRotation.x;
        logoGroup.rotation.y = currentRotation.y;
    }
    
    // Render de scene
    renderer.render(scene, camera);
}
