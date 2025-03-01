/**
 * Lynxx Business Portal - Lynxx Logo Model Generator
 * 
 * Dit bestand bevat functies om een 3D Lynxx logo te genereren met Three.js geometrie.
 * Het logo bestaat uit 3D letters met materialendie passen bij de Lynxx huisstijl.
 */

/**
 * Genereert een 3D Lynxx logo en retourneert een Three.js Group object
 * met alle letters gepositioneerd als één logo.
 * 
 * @param {Object} options Configuratie-opties voor het logo
 * @param {number} options.depth Diepte van de letters (default: 0.2)
 * @param {string} options.color Kleur van het logo (default: '#0099ff')
 * @param {number} options.letterSpacing Afstand tussen de letters (default: 0.1)
 * @param {boolean} options.bevel Of de letters een bevel moeten hebben (default: true)
 * @returns {THREE.Group} Een Three.js Group object met alle letters van het logo
 */
function createLynxxLogoModel(options = {}) {
    // Default opties
    const config = {
        depth: options.depth || 0.2,
        color: options.color || '#0099ff',
        letterSpacing: options.letterSpacing || 0.1,
        bevel: options.bevel !== undefined ? options.bevel : true,
        bevelSize: options.bevelSize || 0.02,
        bevelThickness: options.bevelThickness || 0.02
    };
    
    // Maak een nieuwe groep om alle letters in te plaatsen
    const logoGroup = new THREE.Group();
    
    // Materialen voor de letters
    const mainMaterial = new THREE.MeshPhongMaterial({ 
        color: new THREE.Color(config.color),
        shininess: 70,
        specular: 0x333333
    });
    
    // Parameters voor bevel indien ingeschakeld
    const bevelSettings = config.bevel ? {
        bevelEnabled: true,
        bevelSegments: 3,
        bevelSize: config.bevelSize,
        bevelThickness: config.bevelThickness
    } : { bevelEnabled: false };
    
    // De letters van "LYNXX" opbouwen
    createLetterL(logoGroup, mainMaterial, config, bevelSettings);
    createLetterY(logoGroup, mainMaterial, config, bevelSettings);
    createLetterN(logoGroup, mainMaterial, config, bevelSettings);
    createLetterX(logoGroup, mainMaterial, config, bevelSettings, 1); // Eerste X
    createLetterX(logoGroup, mainMaterial, config, bevelSettings, 2); // Tweede X
    
    // Centreer het logo
    logoGroup.position.x = -2; // Offset om het hele logo te centreren
    
    return logoGroup;
}

/**
 * Creëert een 3D "L" letter en voegt het toe aan de logoGroup
 */
function createLetterL(logoGroup, material, config, bevelSettings) {
    // Maak shape voor letter L
    const lShape = new THREE.Shape();
    lShape.moveTo(0, 0);
    lShape.lineTo(0, 1);
    lShape.lineTo(0.2, 1);
    lShape.lineTo(0.2, 0.2);
    lShape.lineTo(0.7, 0.2);
    lShape.lineTo(0.7, 0);
    lShape.lineTo(0, 0);
    
    // Maak 3D geometrie van de shape
    const geometry = new THREE.ExtrudeGeometry(lShape, {
        depth: config.depth,
        ...bevelSettings
    });
    
    // Maak mesh en voeg toe aan de groep
    const lMesh = new THREE.Mesh(geometry, material);
    lMesh.position.x = 0;
    logoGroup.add(lMesh);
}

/**
 * Creëert een 3D "Y" letter en voegt het toe aan de logoGroup
 */
function createLetterY(logoGroup, material, config, bevelSettings) {
    // Maak shape voor letter Y
    const yShape = new THREE.Shape();
    yShape.moveTo(0, 1);
    yShape.lineTo(0.2, 1);
    yShape.lineTo(0.4, 0.5);
    yShape.lineTo(0.6, 1);
    yShape.lineTo(0.8, 1);
    yShape.lineTo(0.5, 0.3);
    yShape.lineTo(0.5, 0);
    yShape.lineTo(0.3, 0);
    yShape.lineTo(0.3, 0.3);
    yShape.lineTo(0, 1);
    
    // Maak 3D geometrie van de shape
    const geometry = new THREE.ExtrudeGeometry(yShape, {
        depth: config.depth,
        ...bevelSettings
    });
    
    // Maak mesh en voeg toe aan de groep
    const yMesh = new THREE.Mesh(geometry, material);
    yMesh.position.x = 0.8 + config.letterSpacing;
    logoGroup.add(yMesh);
}

/**
 * Creëert een 3D "N" letter en voegt het toe aan de logoGroup
 */
function createLetterN(logoGroup, material, config, bevelSettings) {
    // Maak shape voor letter N
    const nShape = new THREE.Shape();
    nShape.moveTo(0, 0);
    nShape.lineTo(0, 1);
    nShape.lineTo(0.2, 1);
    nShape.lineTo(0.2, 0.3);
    nShape.lineTo(0.6, 1);
    nShape.lineTo(0.8, 1);
    nShape.lineTo(0.8, 0);
    nShape.lineTo(0.6, 0);
    nShape.lineTo(0.6, 0.7);
    nShape.lineTo(0.2, 0);
    nShape.lineTo(0, 0);
    
    // Maak 3D geometrie van de shape
    const geometry = new THREE.ExtrudeGeometry(nShape, {
        depth: config.depth,
        ...bevelSettings
    });
    
    // Maak mesh en voeg toe aan de groep
    const nMesh = new THREE.Mesh(geometry, material);
    nMesh.position.x = 1.7 + (config.letterSpacing * 2);
    logoGroup.add(nMesh);
}

/**
 * Creëert een 3D "X" letter en voegt het toe aan de logoGroup
 * @param {number} instance 1 voor de eerste X, 2 voor de tweede X
 */
function createLetterX(logoGroup, material, config, bevelSettings, instance = 1) {
    // Maak shape voor letter X (bovenste deel)
    const xUpperShape = new THREE.Shape();
    xUpperShape.moveTo(0, 1);
    xUpperShape.lineTo(0.2, 1);
    xUpperShape.lineTo(0.4, 0.6);
    xUpperShape.lineTo(0.6, 1);
    xUpperShape.lineTo(0.8, 1);
    xUpperShape.lineTo(0.5, 0.5);
    xUpperShape.lineTo(0.8, 0);
    xUpperShape.lineTo(0.6, 0);
    xUpperShape.lineTo(0.4, 0.4);
    xUpperShape.lineTo(0.2, 0);
    xUpperShape.lineTo(0, 0);
    xUpperShape.lineTo(0.3, 0.5);
    xUpperShape.lineTo(0, 1);
    
    // Maak 3D geometrie van de shape
    const geometry = new THREE.ExtrudeGeometry(xUpperShape, {
        depth: config.depth,
        ...bevelSettings
    });
    
    // Maak mesh en voeg toe aan de groep
    const xMesh = new THREE.Mesh(geometry, material);
    
    // Positioneer op basis van eerste of tweede X
    if (instance === 1) {
        xMesh.position.x = 2.6 + (config.letterSpacing * 3);
    } else {
        xMesh.position.x = 3.5 + (config.letterSpacing * 4);
    }
    
    logoGroup.add(xMesh);
}
