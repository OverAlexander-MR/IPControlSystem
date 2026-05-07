// Aplicación principal
class PendulumApp {
  constructor() {
    this.simulator = new PendulumSimulator();
    this.isRunning = false;
    this.animationId = null;
    this.lastTimestamp = 0;

    // Backend configuration
    // IMPORTANT: Replace this with your Cloudflare Tunnel URL in production
    this.backendUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? 'http://localhost:8000'
      : 'https://api.ipcontrolsystem.pages.dev';

    this.initElements();
    this.initEventListeners();
    this.initCanvas();

    // Initial check and periodic health check
    this.checkBackendConnection();
    setInterval(() => this.checkBackendConnection(), 5000);

    // Start UI update loops
    this.updateStats();
  }

  initElements() {
    // Sidebar
    this.sidebar = document.getElementById("sidebar");
    this.toggleBtn = document.getElementById("toggleBtn");

    // Navegación
    this.navBtns = document.querySelectorAll(".nav-btn[data-page]");
    this.pages = {
      home: document.getElementById("homePage"),
      pendulum: document.getElementById("pendulumPage"),
      train: document.getElementById("trainPage"),
      graphs: document.getElementById("graphsPage"),
    };

    // Controles del péndulo
    this.controlType = document.getElementById("controlType");
    this.comPort = document.getElementById("comPort");
    this.runBtn = document.getElementById("runBtn");
    this.stopBtn = document.getElementById("stopBtn");
    this.trainBtn = document.getElementById("trainBtn");
    this.exitBtn = document.getElementById("exitBtn");
    this.connectionStatus = document.getElementById("connectionStatus");

    // Estadísticas
    this.positionVal = document.getElementById("positionVal");
    this.velocityVal = document.getElementById("velocityVal");
    this.angleVal = document.getElementById("angleVal");
    this.angularVelVal = document.getElementById("angularVelVal");
  }

  initEventListeners() {
    // Toggle sidebar
    this.toggleBtn.addEventListener("click", () => this.toggleSidebar());

    // Navegación
    this.navBtns.forEach((btn) => {
      btn.addEventListener("click", (e) => this.navigateTo(btn.dataset.page));
    });

    // Controles del péndulo
    this.controlType.addEventListener("change", (e) => {
      this.simulator.setControlType(e.target.value);
      console.log(`Control type changed to: ${e.target.value}`);
      this.sendControlData();
    });

    this.comPort.addEventListener("change", (e) => {
      console.log(`COM port selected: ${e.target.value}`);
      this.sendControlData();
    });

    this.runBtn.addEventListener("click", () => this.startSimulation());
    this.stopBtn.addEventListener("click", () => this.stopSimulation());

    this.trainBtn.addEventListener("click", () => {
      console.log("Training started");
      alert("Entrenamiento iniciado (simulación)");
    });

    this.exitBtn.addEventListener("click", () => {
      if (confirm("¿Estás seguro de que quieres salir?")) {
        this.stopSimulation();
        window.close();
      }
    });
  }

  async checkBackendConnection() {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 2000);
      const response = await fetch(`${this.backendUrl}/health`, { signal: controller.signal });
      clearTimeout(timeoutId);
      
      if (response.ok) {
        this.updateStatusIndicator(true);
      } else {
        this.updateStatusIndicator(false);
      }
    } catch (error) {
      this.updateStatusIndicator(false);
    }
  }

  updateStatusIndicator(connected) {
    if (!this.connectionStatus) return;
    const dot = this.connectionStatus.querySelector(".status-dot");
    const text = this.connectionStatus.querySelector(".status-text");

    if (connected) {
      dot.style.backgroundColor = "#50fa7b";
      text.textContent = "Local Backend: Connected";
    } else {
      dot.style.backgroundColor = "#ff5555";
      text.textContent = "Local Backend: Disconnected";
    }
  }

  async sendControlData() {
    const data = {
      control_type: this.controlType.value,
      com_port: this.comPort.value
    };

    try {
      const response = await fetch(`${this.backendUrl}/control`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        this.updateStatusIndicator(true);
      } else {
        this.updateStatusIndicator(false);
      }
    } catch (error) {
      this.updateStatusIndicator(false);
    }
  }

  initCanvas() {
    this.canvas = document.getElementById("pendulumCanvas");
    if (!this.canvas) return;
    this.drawer = new PendulumDrawer(this.canvas);

    const graphsCanvas = document.getElementById("graphsCanvas");
    if (graphsCanvas) this.initGraphs(graphsCanvas);
  }

  initGraphs(canvas) {
    const ctx = canvas.getContext("2d");
    canvas.width = 800; canvas.height = 400;
    ctx.fillStyle = "#282a36"; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "#bd93f9"; ctx.lineWidth = 2; ctx.beginPath();
    for (let i = 0; i <= 100; i++) {
      const x = i * 8; const y = 200 + 50 * Math.sin(i * 0.1);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  toggleSidebar() {
    this.sidebar.classList.toggle("collapsed");
    const isExpanded = !this.sidebar.classList.contains("collapsed");
    document.querySelectorAll(".nav-text").forEach((text) => {
      text.style.display = isExpanded ? "inline" : "none";
    });
  }

  navigateTo(pageId) {
    Object.values(this.pages).forEach((page) => { if (page) page.classList.add("hidden"); });
    const page = this.pages[pageId];
    if (page) page.classList.remove("hidden");

    this.navBtns.forEach((btn) => {
      btn.classList.remove("active");
      if (btn.dataset.page === pageId) btn.classList.add("active");
    });

    if (pageId !== "pendulum" && this.isRunning) this.stopSimulation();

    if (pageId === "pendulum" && this.simulator) {
      setTimeout(() => {
        const state = this.simulator.next(0);
        if (this.drawer) this.drawer.draw(state.cartPos, state.theta);
      }, 100);
    }
  }

  startSimulation() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.simulator.reset();
    this.simulator.setControlType(this.controlType.value);
    this.lastTimestamp = performance.now();
    this.simulationLoop();
    this.sendControlData();
  }

  stopSimulation() {
    this.isRunning = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  simulationLoop() {
    if (!this.isRunning) return;
    const now = performance.now();
    let dt = Math.min(0.033, (now - this.lastTimestamp) / 1000);
    if (dt > 0.001) {
      const state = this.simulator.next(dt);
      this.drawer.draw(state.cartPos, state.theta);
      this.updateStatsDisplay(state);
      this.lastTimestamp = now;
    }
    this.animationId = requestAnimationFrame(() => this.simulationLoop());
  }

  updateStats() {
    if (!this.isRunning && this.simulator) {
        const state = this.simulator.next(0);
        this.updateStatsDisplay(state);
        if (this.drawer && !this.pages.pendulum.classList.contains("hidden")) {
            this.drawer.draw(state.cartPos, state.theta);
        }
    }
    requestAnimationFrame(() => this.updateStats());
  }

  updateStatsDisplay(state) {
    if (this.positionVal) {
      this.positionVal.textContent = state.cartPos.toFixed(3);
      this.velocityVal.textContent = state.cartVel.toFixed(3);
      this.angleVal.textContent = ((state.theta * 180) / Math.PI).toFixed(1) + "°";
      this.angularVelVal.textContent = state.thetaDot.toFixed(3);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const app = new PendulumApp();
});
