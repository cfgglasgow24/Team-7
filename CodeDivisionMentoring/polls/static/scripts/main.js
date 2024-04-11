/*$(document).ready(function() {

  function toggleSidebar() {
    $(".button").toggleClass("active");
    $("main").toggleClass("move-to-left");
    $(".sidebar-item").toggleClass("active");
  }

  $(".button").on("click tap", function() {
    toggleSidebar();
  });

  $(document).keyup(function(e) {
    if (e.keyCode === 27) {
      toggleSidebar();
    }
  });

});*/
function hello(){
  console.log("hello there")
}
function toggleSidenav() {
  var sidenav = document.querySelector('.sidenav');
  sidenav.classList.toggle('active');
}

/*-----------------------------------REGISTRO-----------------------------------*/

/*const form = document.querySelector('form');
const inputNombre = document.querySelector('#input1');
const inputApellidos = document.querySelector('#input2');
const inputUsername = document.querySelector('#input3');
const inputCiudad = document.querySelector('#input4');
const inputEstado = document.querySelector('#input5');
const inputCodigoPostal = document.querySelector('#input6');
const inputTerminos = document.querySelector('#input7');

// Función para comprobar si el valor de entrada es válido o no
function esValido(input) {
  return input.value.trim() !== '';
}

// Función para cambiar el color del campo de entrada según sea válido o no
function cambiarColor(input) {
  if (esValido(input)) {
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
  } else {
    input.classList.remove('is-valid');
    input.classList.add('is-invalid');
  }
}

// Evento de validación de entrada para el campo de nombre
inputNombre.addEventListener('blur', function() {
  cambiarColor(inputNombre);
});

// Evento de validación de entrada para el campo de apellidos
inputApellidos.addEventListener('blur', function() {
  cambiarColor(inputApellidos);
});

// Evento de validación de entrada para el campo de nombre de usuario
inputUsername.addEventListener('blur', function() {
  cambiarColor(inputUsername);
});

// Evento de validación de entrada para el campo de ciudad
inputCiudad.addEventListener('blur', function() {
  cambiarColor(inputCiudad);
});

// Evento de validación de entrada para el campo de estado
inputEstado.addEventListener('blur', function() {
  cambiarColor(inputEstado);
});

// Evento de validación de entrada para el campo de código postal
inputCodigoPostal.addEventListener('blur', function() {
  cambiarColor(inputCodigoPostal);
});

// Evento de validación de entrada para el campo de términos y condiciones
inputTerminos.addEventListener('change', function() {
  cambiarColor(inputTerminos);
});

// Evento de envío del formulario
form.addEventListener('submit', function(event) {
  // Comprobar si todos los campos de entrada son válidos
  if (!esValido(inputNombre) || !esValido(inputApellidos) || !esValido(inputUsername) || !esValido(inputCiudad) || !esValido(inputEstado) || !esValido(inputCodigoPostal) || !inputTerminos.checked) {
    // Si no son válidos, detener el envío del formulario
    event.preventDefault();
  }
});*/