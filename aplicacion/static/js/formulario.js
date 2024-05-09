document.addEventListener("DOMContentLoaded", function() {
  // const form = document.querySelector('form');
  // const formInputs = document.querySelectorAll(".br-input");

  // function actualizarProgreso() {
  //   let answeredQuestions = 0; // Contador para preguntas respondidas
  //   formInputs.forEach(input => {
  //       if (input.type === 'radio' || input.type === 'checkbox') {
  //           if (input.checked) {
  //               answeredQuestions++; // Incrementa el contador cuando se responde una pregunta
  //           }
  //       } else if (input.value !== '') { // Verifica si el campo no está vacío
  //           answeredQuestions++; // Incrementa el contador cuando se responde una pregunta
  //       }
  //   });
  //   const progreso = Math.round((answeredQuestions / formInputs.length) * 100); // Calcula y redondea el progreso
  //   actualizarBarraDeProgreso(progreso); // Actualiza la barra de progreso
  // }

  // // Función para guardar los datos del formulario en el almacenamiento local
  // function guardarDatosFormulario(valor) {
  //   localStorage.setItem(valor.id, valor.value);
  // }

  // // Función para cargar los datos del almacenamiento local y rellenar el formulario
  // function cargarDatosFormulario() {
  //     formInputs.forEach(input => {
  //         const savedValue = localStorage.getItem(input.id);
  //         if (savedValue !== null) {
  //             input.value = savedValue;
  //         }
  //     });
  //     console.log("bb");
  // }

  // // Cargar datos del formulario al cargar la página
  // cargarDatosFormulario();

  // // Eliminar datos del almacenamiento local cuando se envía el formulario o se cancela
  // form.addEventListener('submit', function() {
  //     localStorage.clear();
  // });

  // form.addEventListener('reset', function() {
  //     localStorage.clear();
  // });

  // formInputs.forEach(input => {
  //   input.addEventListener('input', () => {
  //     actualizarProgreso();
  //     guardarDatosFormulario(input);
  //   });
  // });

  // function actualizarBarraDeProgreso(pasoActual) {
  //   const barraDeProgreso = document.getElementById('barra-porcentaje');
  //   barraDeProgreso.style.width = `${pasoActual}%`;
  //   barraDeProgreso.innerText = `${pasoActual}%`;

  //   // Cambiar color de fondo según el progreso
  //   if (pasoActual <= (100 / 3)) {
  //     barraDeProgreso.style.backgroundColor = 'red'; // Menor o igual a 1/3
  //   } else if (pasoActual > (100 / 3) && pasoActual <= (200 / 3)) {
  //     barraDeProgreso.style.backgroundColor = 'orange'; // Mayor a 1/3 y menor o igual a 2/3
  //   } else {
  //     barraDeProgreso.style.backgroundColor = 'green'; // Mayor a 2/3
  //   }
  // }

  // actualizarProgreso();
  
  const totalPasos = document.querySelectorAll('.step').length;
  const steps = document.querySelectorAll(".stp");
  const circleSteps = document.querySelectorAll(".step");
  const inputs = document.querySelectorAll(".step-1 form input");
  let currentStep = 1;
  let currentCircle = 0;

  steps.forEach((step) => {
    const nextBtn = step.querySelector(".next-stp");
    const prevBtn = step.querySelector(".prev-stp");
    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        document.querySelector(`.step-${currentStep}`).style.display = "none";
        currentStep--;
        document.querySelector(`.step-${currentStep}`).style.display = "flex";
        circleSteps[currentCircle].classList.remove("active");
        currentCircle--;
      });
    }
    nextBtn.addEventListener("click", () => {
      document.querySelector(`.step-${currentStep}`).style.display = "none";
      if (currentStep < totalPasos && validateForm()) {
        currentStep++;
        currentCircle++;
      }
      document.querySelector(`.step-${currentStep}`).style.display = "flex";
      circleSteps[currentCircle].classList.add("active");
    });
  });

  function validateForm() {
    let valid = true;
    inputs.forEach(input => {
      if (!input.value) {
        valid = false;
        input.classList.add("err");
        findLabel(input).nextElementSibling.style.display = "flex";
      } else {
        input.classList.remove("err");
        findLabel(input).nextElementSibling.style.display = "none";
      }
    });
    return valid;
  }

  function findLabel(el) {
    const idVal = el.id;
    const labels = document.getElementsByTagName("label");
    for (let i = 0; i < labels.length; i++) {
      if (labels[i].htmlFor === idVal) return labels[i];
    }
  }
});



// Funcion para activar circle
function activateCircleStep(stepNumber) {
  const circleSteps = document.querySelectorAll(".step");
  circleSteps.forEach(circle => {
      circle.classList.remove("active");
  });
  circleSteps[stepNumber - 1].classList.add("active");
}