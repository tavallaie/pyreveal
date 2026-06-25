import * as THREE from "three";

const INK = 0x08090c;
const LINE_RGB = [0.72, 0.78, 0.86];
const TIME_SCALE = 0.85;

let active = null;

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function smoothWave(x, y, t) {
  const a = Math.sin(x * 0.42 + t * 0.62) * Math.cos(y * 0.38 + t * 0.48);
  const b = Math.sin(y * 0.55 - t * 0.36 + x * 0.22) * 0.72;
  const c = Math.sin((x + y) * 0.26 + t * 0.28) * 0.48;
  const d = Math.cos(x * 0.18 - y * 0.24 + t * 0.2) * 0.35;
  return (a + b + c + d) * 1.15;
}

function edgeSeed(n) {
  const x = Math.sin(n * 127.1) * 43758.5453;
  return x - Math.floor(x);
}

class FlowMesh3D {
  constructor(canvas) {
    this.canvas = canvas;
    this.clock = new THREE.Clock();
    this.mobile = window.innerWidth < 768;
    this.reducedMotion = prefersReducedMotion();
    this._onResize = () => this._resize();

    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: false,
      powerPreference: "high-performance",
      failIfMajorPerformanceCaveat: false,
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setClearColor(INK, 1);

    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.Fog(INK, 18, 48);

    this.camera = new THREE.PerspectiveCamera(48, 1, 0.1, 80);

    this.group = new THREE.Group();
    this.scene.add(this.group);

    this._buildSurface();
    this._resize();
    window.addEventListener("resize", this._onResize, { passive: true });

    this._tick = this._tick.bind(this);
    if (!this.reducedMotion) {
      this.raf = requestAnimationFrame(this._tick);
    } else {
      this._updateMesh(0);
      this.renderer.render(this.scene, this.camera);
    }
  }

  _segments() {
    return this.mobile
      ? { x: 52, y: 36 }
      : { x: 80, y: 54 };
  }

  _buildSurface() {
    if (this.lines) {
      this.group.remove(this.lines);
      this.lines.geometry.dispose();
      this.lines.material.dispose();
    }

    const { x: segX, y: segY } = this._segments();
    const plane = new THREE.PlaneGeometry(34, 22, segX, segY);
    this.basePositions = Float32Array.from(plane.attributes.position.array);
    plane.dispose();

    this.cols = segX + 1;
    this.rows = segY + 1;
    this.vertexCount = this.cols * this.rows;
    this.vertexPositions = new Float32Array(this.vertexCount * 3);

    const pairList = [];

    for (let j = 0; j <= segY; j += 1) {
      for (let i = 0; i < segX; i += 1) {
        pairList.push(i + j * this.cols, i + 1 + j * this.cols);
      }
    }

    for (let i = 0; i <= segX; i += 1) {
      for (let j = 0; j < segY; j += 1) {
        pairList.push(i + j * this.cols, i + (j + 1) * this.cols);
      }
    }

    this.edgePairs = new Uint32Array(pairList);
    this.edgeCount = this.edgePairs.length / 2;
    this.edgePhases = new Float32Array(this.edgeCount);
    this.edgeRates = new Float32Array(this.edgeCount);

    for (let e = 0; e < this.edgeCount; e += 1) {
      this.edgePhases[e] = edgeSeed(e * 1.73) * Math.PI * 2;
      this.edgeRates[e] = 1.4 + edgeSeed(e * 2.19) * 2.6;
    }

    const linePositions = new Float32Array(this.edgeCount * 6);
    const lineColors = new Float32Array(this.edgeCount * 6);
    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute("position", new THREE.BufferAttribute(linePositions, 3));
    lineGeometry.setAttribute("color", new THREE.BufferAttribute(lineColors, 3));

    const lineMaterial = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.82,
      depthWrite: false,
    });

    this.lines = new THREE.LineSegments(lineGeometry, lineMaterial);
    this.lines.rotation.x = -Math.PI * 0.36;
    this.group.add(this.lines);
  }

  _edgeBrightness(t, edgeIndex) {
    if (this.reducedMotion) {
      return 0.42;
    }

    const pulse = Math.sin(t * this.edgeRates[edgeIndex] + this.edgePhases[edgeIndex]);
    if (pulse < 0.08) {
      return 0;
    }

    return 0.32 + (pulse - 0.08) * 0.52;
  }

  _updateMesh(t) {
    const base = this.basePositions;
    const verts = this.vertexPositions;

    for (let i = 0; i < this.vertexCount; i += 1) {
      const x = base[i * 3];
      const y = base[i * 3 + 1];
      verts[i * 3] = x;
      verts[i * 3 + 1] = y;
      verts[i * 3 + 2] = smoothWave(x, y, t);
    }

    const positions = this.lines.geometry.attributes.position.array;
    const colors = this.lines.geometry.attributes.color.array;

    for (let e = 0; e < this.edgeCount; e += 1) {
      const a = this.edgePairs[e * 2];
      const b = this.edgePairs[e * 2 + 1];
      const p = e * 6;

      positions[p] = verts[a * 3];
      positions[p + 1] = verts[a * 3 + 1];
      positions[p + 2] = verts[a * 3 + 2];
      positions[p + 3] = verts[b * 3];
      positions[p + 4] = verts[b * 3 + 1];
      positions[p + 5] = verts[b * 3 + 2];

      const brightness = this._edgeBrightness(t, e);
      for (let k = 0; k < 2; k += 1) {
        const c = p + k * 3;
        colors[c] = LINE_RGB[0] * brightness;
        colors[c + 1] = LINE_RGB[1] * brightness;
        colors[c + 2] = LINE_RGB[2] * brightness;
      }
    }

    this.lines.geometry.attributes.position.needsUpdate = true;
    this.lines.geometry.attributes.color.needsUpdate = true;
  }

  _layout(aspect) {
    const dist = 15.5;
    const vFov = (48 * Math.PI) / 180;
    const visibleH = 2 * dist * Math.tan(vFov / 2);
    const cover = 1.2;

    this.camera.position.set(0, visibleH * 0.18, dist);
    this.camera.lookAt(0, -1.15, 0);

    this.group.position.set(0, -1.55, 0);
    this.group.scale.set(aspect * cover * 0.62, cover, 1);
  }

  _resize() {
    const width = Math.max(window.innerWidth, 1);
    const height = Math.max(window.innerHeight, 1);

    if (width < 2 || height < 2) {
      requestAnimationFrame(() => this._resize());
      return;
    }

    const mobile = width < 768;
    if (mobile !== this.mobile) {
      this.mobile = mobile;
      this._buildSurface();
    }

    const aspect = width / height;
    this._layout(aspect);
    this.camera.aspect = aspect;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height, false);
  }

  _tick() {
    const t = this.clock.getElapsedTime() * TIME_SCALE;

    this._updateMesh(t);
    this.group.rotation.y = Math.sin(t * 0.18) * 0.1;
    this.group.rotation.z = Math.sin(t * 0.11) * 0.018;

    this.renderer.render(this.scene, this.camera);
    this.raf = requestAnimationFrame(this._tick);
  }

  dispose() {
    if (this.raf) cancelAnimationFrame(this.raf);
    window.removeEventListener("resize", this._onResize);

    this.scene.traverse((object) => {
      if (object.geometry) object.geometry.dispose();
      if (object.material) {
        if (Array.isArray(object.material)) {
          object.material.forEach((m) => m.dispose());
        } else {
          object.material.dispose();
        }
      }
    });
    this.renderer.dispose();
  }
}

function destroy() {
  if (active) {
    active.dispose();
    active = null;
  }
}

function init() {
  const canvas = document.getElementById("home-hero-canvas");
  if (!canvas) {
    destroy();
    return;
  }

  destroy();
  document.body.classList.remove("no-hero-webgl");

  try {
    active = new FlowMesh3D(canvas);
  } catch (error) {
    console.warn("Home hero WebGL failed:", error);
    document.body.classList.add("no-hero-webgl");
  }
}

if (typeof document$ !== "undefined") {
  document$.subscribe(init);
}
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}