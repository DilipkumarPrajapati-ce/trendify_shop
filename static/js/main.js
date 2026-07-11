// Initialize Three.js Engine Canvas when on Home View
const container = document.getElementById('canvas-3d-container');

if (container) {
    // 1. Scene setup
    const scene = new THREE.Scene();

    // 2. Camera Configuration Setup
   //  CORRECT (Changed '01' to '0.1')
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 3;

    // 3. WebGL Renderer Initialization
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // 4. Object Geometry Definition (A geometric mesh representation of a 3D clothing placeholder showcase)
    const geometry = new THREE.TorusKnotGeometry(0.6, 0.2, 100, 16);
    const material = new THREE.MeshNormalMaterial();
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    // 5. Continuous Frame Animation Loop Execution
    function animate() {
        requestAnimationFrame(animate);
        
        // Rotational motion parameters on ticks
        mesh.rotation.x += 0.01;
        mesh.rotation.y += 0.01;
        
        renderer.render(scene, camera);
    }
    
    animate();

    // Dynamically adjust render viewport sizing on screen resolution variance
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}
   
