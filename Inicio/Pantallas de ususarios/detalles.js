const selectedSpace = JSON.parse(localStorage.getItem("selectedSpace"));

if (selectedSpace) {

  document.getElementById("space-image").src = selectedSpace.image;
  document.getElementById("space-title").textContent = selectedSpace.title;
  document.getElementById("space-description").textContent = `Ubicación: ${selectedSpace.location}. Precio: ${selectedSpace.price}.`;
} else {
  // Manejar el caso en el que no haya datos seleccionados
  document.querySelector(".container").innerHTML = `
    <p>Ocurrió un error al cargar los detalles del espacio. Regresa al catálogo y selecciona un espacio nuevamente.</p>
  `;
}
document.getElementById("confirm-button").addEventListener("click", function (event) {
  event.preventDefault();
  window.location.href = "pago.html";
});
