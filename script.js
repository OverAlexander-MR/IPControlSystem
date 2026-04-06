function showView(viewId) {
  document
    .querySelectorAll(".view")
    .forEach((v) => v.classList.remove("active"));
  document.getElementById(viewId).classList.add("active");
}

// Simulación de backend
async function enviarComando() {
  const res = await fetch("https://api.primbiolab.org/test"); // luego lo creamos
  const data = await res.json();
  document.getElementById("respuesta").innerText = data.mensaje;
}
