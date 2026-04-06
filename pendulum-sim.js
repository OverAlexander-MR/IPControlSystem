// Simulador físico del péndulo invertido
class PendulumSimulator {
  constructor() {
    // Parámetros físicos
    this.M = 1.0; // masa del carro (kg)
    this.m = 0.1; // masa del péndulo (kg)
    this.l = 0.5; // longitud (m)
    this.g = 9.81; // gravedad (m/s²)
    this.b = 0.0; // fricción (N/m/s)
    this.trackHalfRange = 2.0; // rango de la pista (m)

    // Estado inicial
    this.x = 0.0;
    this.xDot = 0.0;
    this.theta = 0.05; // pequeña inclinación inicial
    this.thetaDot = 0.0;
    this.t = 0.0;

    // Control
    this.controlFunc = null;
    this.controlType = "LQR";

    // Ganancia LQR (simplificada)
    this.K = [-1.5, -2.5, 35, 8]; // [x, x_dot, theta, theta_dot]
  }

  setControlType(type) {
    this.controlType = type;
    if (type === "LQR") {
      this.K = [-1.5, -2.5, 35, 8];
    } else if (type === "LQR + Swim up") {
      this.K = [-1.8, -3.0, 40, 10];
    } else if (type === "SAC") {
      this.K = [-1.2, -2.0, 30, 6];
    } else if (type === "DDPG") {
      this.K = [-1.6, -2.8, 38, 9];
    }
  }

  computeControl(state, t) {
    const [x, xDot, theta, thetaDot] = state;

    if (this.controlType === "LQR + Swim up" && Math.abs(theta) > 0.5) {
      // Estrategia de "swim up" - energía creciente
      const energyTarget = 2 * this.m * this.g * this.l;
      const energy =
        0.5 * this.m * Math.pow(this.l * thetaDot, 2) +
        this.m * this.g * this.l * (1 - Math.cos(theta));
      const energyError = energyTarget - energy;
      return Math.min(10, Math.max(-10, 2 * energyError * Math.cos(theta)));
    }

    // Control LQR estándar
    let force = 0;
    force += this.K[0] * x;
    force += this.K[1] * xDot;
    force += this.K[2] * theta;
    force += this.K[3] * thetaDot;

    return Math.min(15, Math.max(-15, force));
  }

  derivatives(state, t, F) {
    const [x, xDot, theta, thetaDot] = state;
    const M = this.M;
    const m = this.m;
    const l = this.l;
    const g = this.g;
    const b = this.b;

    const sinTheta = Math.sin(theta);
    const cosTheta = Math.cos(theta);

    const denom = l * (4 / 3 - (m * cosTheta * cosTheta) / (M + m));
    const thetaNum =
      g * sinTheta +
      cosTheta *
        ((-F - m * l * thetaDot * thetaDot * sinTheta + b * xDot) / (M + m));
    const thetaDDot = thetaNum / denom;
    const xDDot =
      (F +
        m * l * (thetaDot * thetaDot * sinTheta - thetaDDot * cosTheta) -
        b * xDot) /
      (M + m);

    return [xDot, xDDot, thetaDot, thetaDDot];
  }

  rk4Step(dt) {
    const state0 = [this.x, this.xDot, this.theta, this.thetaDot];
    const t0 = this.t;

    let F0 = 0;
    if (this.controlFunc) {
      F0 = this.controlFunc(state0, t0);
    } else {
      F0 = this.computeControl(state0, t0);
    }

    const k1 = this.derivatives(state0, t0, F0);
    const s1 = state0.map((val, i) => val + 0.5 * dt * k1[i]);
    const F1 = this.controlFunc
      ? this.controlFunc(s1, t0 + 0.5 * dt)
      : this.computeControl(s1, t0 + 0.5 * dt);
    const k2 = this.derivatives(s1, t0 + 0.5 * dt, F1);

    const s2 = state0.map((val, i) => val + 0.5 * dt * k2[i]);
    const F2 = this.controlFunc
      ? this.controlFunc(s2, t0 + 0.5 * dt)
      : this.computeControl(s2, t0 + 0.5 * dt);
    const k3 = this.derivatives(s2, t0 + 0.5 * dt, F2);

    const s3 = state0.map((val, i) => val + dt * k3[i]);
    const F3 = this.controlFunc
      ? this.controlFunc(s3, t0 + dt)
      : this.computeControl(s3, t0 + dt);
    const k4 = this.derivatives(s3, t0 + dt, F3);

    const newState = state0.map(
      (val, i) => val + (dt / 6) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]),
    );

    [this.x, this.xDot, this.theta, this.thetaDot] = newState;
    this.t += dt;

    // Normalizar theta a [-π, π]
    while (this.theta > Math.PI) this.theta -= 2 * Math.PI;
    while (this.theta < -Math.PI) this.theta += 2 * Math.PI;
  }

  next(dt) {
    // Sub-pasos para estabilidad
    const maxSubstep = 0.02;
    const steps = Math.max(1, Math.ceil(dt / maxSubstep));
    const subDt = dt / steps;

    for (let i = 0; i < steps; i++) {
      this.rk4Step(subDt);
    }

    // Normalizar posición
    let xNorm = this.x / this.trackHalfRange;
    xNorm = Math.max(-1, Math.min(1, xNorm));

    return {
      cartPos: xNorm,
      cartVel: this.xDot,
      theta: this.theta,
      thetaDot: this.thetaDot,
    };
  }

  reset() {
    this.x = 0;
    this.xDot = 0;
    this.theta = 0.05;
    this.thetaDot = 0;
    this.t = 0;
  }
}

// Dibujador del péndulo
class PendulumDrawer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.resizeCanvas();
    window.addEventListener("resize", () => this.resizeCanvas());
  }

  resizeCanvas() {
    const container = this.canvas.parentElement;
    const rect = container.getBoundingClientRect();
    this.canvas.width = Math.min(800, rect.width - 40);
    this.canvas.height = 400;
  }

  draw(cartPos, theta) {
    const w = this.canvas.width;
    const h = this.canvas.height;
    const ctx = this.ctx;

    // Limpiar canvas
    ctx.clearRect(0, 0, w, h);

    // Configurar colores (Dracula)
    const colors = {
      muted: "#6272a4",
      panel: "#21222c",
      currentLine: "#44475a",
      fg: "#f8f8f2",
      accent: "#bd93f9",
      orange: "#ffb86c",
    };

    // Margen y pista
    const margin = 40;
    const trackLeft = margin;
    const trackRight = w - margin;
    const trackWidth = trackRight - trackLeft;

    // Posición del carro
    const xPix = trackLeft + ((cartPos + 1) / 2) * trackWidth;

    // Dimensiones del carro
    const cartW = Math.min(100, trackWidth * 0.35);
    const cartH = 36;
    const cartX = xPix - cartW / 2;
    const cartY = h * 0.55;

    // Dibujar pista
    ctx.beginPath();
    ctx.strokeStyle = colors.muted;
    ctx.lineWidth = 2;
    ctx.moveTo(trackLeft, cartY + cartH + 20);
    ctx.lineTo(trackRight, cartY + cartH + 20);
    ctx.stroke();

    // Dibujar carro
    ctx.fillStyle = colors.panel;
    ctx.strokeStyle = colors.currentLine;
    ctx.lineWidth = 2;
    ctx.fillRect(cartX, cartY, cartW, cartH);
    ctx.strokeRect(cartX, cartY, cartW, cartH);

    // Dibujar ruedas
    const wheelRadius = 8;
    ctx.fillStyle = colors.muted;
    ctx.beginPath();
    ctx.arc(
      cartX + cartW * 0.22,
      cartY + cartH + wheelRadius,
      wheelRadius,
      0,
      2 * Math.PI,
    );
    ctx.fill();
    ctx.beginPath();
    ctx.arc(
      cartX + cartW * 0.78,
      cartY + cartH + wheelRadius,
      wheelRadius,
      0,
      2 * Math.PI,
    );
    ctx.fill();

    // Pivote
    const pivotX = xPix;
    const pivotY = cartY - 6;

    // Longitud de la varilla
    const rodLength = h * 0.35;

    // Posición de la masa
    const bobX = pivotX + rodLength * Math.sin(theta);
    const bobY = pivotY - rodLength * Math.cos(theta);

    // Dibujar varilla
    ctx.beginPath();
    ctx.strokeStyle = colors.fg;
    ctx.lineWidth = 3;
    ctx.moveTo(pivotX, pivotY);
    ctx.lineTo(bobX, bobY);
    ctx.stroke();

    // Dibujar pivote
    ctx.fillStyle = colors.accent;
    ctx.beginPath();
    ctx.arc(pivotX, pivotY, 5, 0, 2 * Math.PI);
    ctx.fill();

    // Dibujar masa
    const bobRadius = Math.max(10, Math.min(28, h * 0.06));
    ctx.fillStyle = colors.orange;
    ctx.beginPath();
    ctx.arc(bobX, bobY, bobRadius, 0, 2 * Math.PI);
    ctx.fill();
    ctx.strokeStyle = colors.currentLine;
    ctx.stroke();
  }
}
