// Initialize Three.js Engine Canvas when on Home View
const container = document.getElementById('canvas-3d-container');

// If the container explicitly disables 3D (data-disable-3d="true"), skip initializing Three.js
if (container && container.dataset.disable3d !== 'true') {
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
   
    // --- On-demand featured 3D viewer ------------------------------------------------
    function createFeatured3D(imageUrl) {
        const parent = document.getElementById('canvas-3d-container');
        if (!parent) return;

        // hide static image
        const img = document.getElementById('featured-image');
        if (img) img.style.display = 'none';

        // create canvas wrapper
        const canvasWrap = document.createElement('div');
        canvasWrap.id = 'featured-3d-canvas';
        canvasWrap.style.width = '100%';
        canvasWrap.style.height = '420px';
        canvasWrap.style.borderRadius = '12px';
        canvasWrap.style.overflow = 'hidden';
        canvasWrap.style.position = 'relative';
        parent.appendChild(canvasWrap);

        // close button
        const closeBtn = document.createElement('button');
        closeBtn.innerText = 'Close 3D';
        closeBtn.className = 'btn btn--ghost';
        closeBtn.style.position = 'absolute';
        closeBtn.style.right = '18px';
        closeBtn.style.top = '18px';
        closeBtn.style.zIndex = 10;
        canvasWrap.appendChild(closeBtn);

        // three.js basic scene
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(40, canvasWrap.clientWidth / canvasWrap.clientHeight, 0.1, 1000);
        camera.position.set(0, 0, 2.6);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(canvasWrap.clientWidth, canvasWrap.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        canvasWrap.appendChild(renderer.domElement);

        // lights
        const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 1.0);
        scene.add(hemi);
        const dir = new THREE.DirectionalLight(0xffffff, 0.6);
        dir.position.set(5, 10, 7.5);
        scene.add(dir);

        // geometry: slightly rounded box to give 'hoodie' volume
        const geometry = new THREE.BoxGeometry(1.6, 1.6, 0.6, 32, 32, 32);

        // load texture from image URL
        const loader = new THREE.TextureLoader();
        loader.crossOrigin = '';
        loader.load(imageUrl, (texture) => {
            texture.wrapS = texture.wrapT = THREE.ClampToEdgeWrapping;
            const material = new THREE.MeshStandardMaterial({ map: texture, metalness: 0.05, roughness: 0.6 });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.rotation.y = 0.4;
            mesh.rotation.x = -0.12;
            scene.add(mesh);

            // subtle animation
            const clock = new THREE.Clock();
            (function animate() {
                requestAnimationFrame(animate);
                const t = clock.getElapsedTime();
                mesh.rotation.y = 0.4 + Math.sin(t * 0.4) * 0.12;
                renderer.render(scene, camera);
            })();
        }, undefined, (err) => {
            console.error('Texture load failed', err);
        });

        closeBtn.addEventListener('click', () => {
            // remove canvas and show original image
            try { renderer.dispose(); } catch (e) {}
            canvasWrap.remove();
            if (img) img.style.display = 'block';
        });

        // handle resize
        window.addEventListener('resize', () => {
            if (!canvasWrap) return;
            camera.aspect = canvasWrap.clientWidth / canvasWrap.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(canvasWrap.clientWidth, canvasWrap.clientHeight);
        });
    }

    // wire up button (if present) to launch 3D view
    document.addEventListener('DOMContentLoaded', () => {
        const btn = document.getElementById('featured-3d-btn');
        if (btn) {
            btn.addEventListener('click', (e) => {
                const img = document.getElementById('featured-image');
                if (!img) return;
                // pass current image src to 3D viewer
                createFeatured3D(img.src);
            });
        }
    });

