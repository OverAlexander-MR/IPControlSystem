// function showView(viewId) {
//   document
//     .querySelectorAll(".view")
//     .forEach((v) => v.classList.remove("active"));
//   document.getElementById(viewId).classList.add("active");
// }

// // Simulación de backend
// async function enviarComando() {
//   const res = await fetch("https://api.primbiolab.org/test"); // luego lo creamos
//   const data = await res.json();
//   document.getElementById("respuesta").innerText = data.mensaje;
// }

const canvas = document.getElementById("pendulumCanvas");
const ctx = canvas.getContext("2d");

let angle = 0.5;
let velocity = 0;
let running = false;

function resizeCanvas() {
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const cx = canvas.width / 2;
  const cy = canvas.height / 3;
  const length = 150;

  const x = cx + length * Math.sin(angle);
  const y = cy + length * Math.cos(angle);

  // barra
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(x, y);
  ctx.strokeStyle = "white";
  ctx.lineWidth = 3;
  ctx.stroke();

  // bola
  ctx.beginPath();
  ctx.arc(x, y, 20, 0, Math.PI * 2);
  ctx.fillStyle = "#f4a261";
  ctx.fill();

  // base
  ctx.fillStyle = "#444";
  ctx.fillRect(cx - 30, cy + length, 60, 20);
}

function update() {
  if (running) {
    const g = 0.01;
    velocity += -g * Math.sin(angle);
    angle += velocity;
  }
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

loop();

function start() {
  running = true;
}

function stop() {
  running = false;
}
