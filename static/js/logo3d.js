/**
 * Lynxx Business Portal - 3D Logo Animation
 * 
 * Dit bestand bevat de Three.js implementatie voor het 3D-roterende Lynxx-logo.
 * Het logo draait langzaam om zijn X en Y as in de header van de pagina.
 */

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
    
    // Scene, camera en renderer instellen
    const scene = new THREE.Scene();
    
    // Camera instellen met goede verhoudingen voor de container
    const aspectRatio = container.clientWidth / container.clientHeight;
    const camera = new THREE.PerspectiveCamera(75, aspectRatio, 0.1, 1000);
    camera.position.z = 5;
    
    // Renderer instellen met transparante achtergrond
    const renderer = new THREE.WebGLRenderer({ 
        antialias: true,
        alpha: true 
    });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000, 0); // Transparante achtergrond
    container.appendChild(renderer.domElement);
    
    // Belichting instellen
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);
    
    // 3D tekst voor "LYNXX" maken
    const fontLoader = new THREE.FontLoader();
    
    // We gebruiken een standaard font omdat we in deze setup geen externe fonts kunnen laden
    // In de uiteindelijke implementatie zou een custom font kunnen worden gebruikt
    // dat past bij de Lynxx huisstijl
    createTextMesh("LYNXX", scene);
    
    // Animatie-loop starten
    function animate() {
        requestAnimationFrame(animate);
        
        // Roteer alle meshes in de scene (het logo)
        scene.traverse(function(object) {
            if (object.isMesh) {
                // Langzame rotatie om X en Y as
                object.rotation.x += 0.005;
                object.rotation.y += 0.007;
            }
        });
        
        renderer.render(scene, camera);
    }
    
    // Start de animatie
    animate();
    
    // Window resize handler
    window.addEventListener('resize', function() {
        const newWidth = container.clientWidth;
        const newHeight = container.clientHeight;
        
        camera.aspect = newWidth / newHeight;
        camera.updateProjectionMatrix();
        
        renderer.setSize(newWidth, newHeight);
    });
}

/**
 * Creëert een 3D text mesh en voegt het toe aan de scene
 * 
 * @param {string} text De tekst om weer te geven in 3D
 * @param {THREE.Scene} scene De Three.js scene om de tekst aan toe te voegen
 */
function createTextMesh(text, scene) {
    // Omdat we geen FontLoader kunnen gebruiken in deze setup, maken we een eenvoudige kubus
    // als tijdelijke plaatshouder voor het logo.
    // In de volledige implementatie zou dit vervangen worden door de echte 3D tekst.
    
    const geometry = new THREE.BoxGeometry(3, 1, 0.3);
    const material = new THREE.MeshPhongMaterial({ 
        color: 0x0099ff,
        specular: 0x555555,
        shininess: 30
    });
    
    const textMesh = new THREE.Mesh(geometry, material);
    scene.add(textMesh);
    
    // Voeg kleine bollen toe als decoratie (als vervanging van de letters)
    const sphereGeometry = new THREE.SphereGeometry(0.1, 16, 16);
    const sphereMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
    
    // Voeg bollen toe op posities om "LYNXX" te suggereren
    const positions = [
        [-1.0, 0, 0.2],  // L
        [-0.5, 0, 0.2],  // Y
        [0, 0, 0.2],     // N
        [0.5, 0, 0.2],   // X
        [1.0, 0, 0.2],   // X
    ];
    
    positions.forEach(pos => {
        const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
        sphere.position.set(pos[0], pos[1], pos[2]);
        scene.add(sphere);
    });
}