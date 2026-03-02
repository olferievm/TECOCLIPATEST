const steps = Array.from(document.querySelectorAll('.wizard-step'));
const prevButton = document.getElementById('prev-step');
const nextButton = document.getElementById('next-step');
const submitButton = document.getElementById('submit-btn');

let activeStep = 0;

function renderStep() {
  steps.forEach((step, idx) => {
    step.classList.toggle('active', idx === activeStep);
  });
  prevButton.disabled = activeStep === 0;
  const isLast = activeStep === steps.length - 1;
  nextButton.classList.toggle('hidden', isLast);
  submitButton.classList.toggle('hidden', !isLast);
}

prevButton?.addEventListener('click', () => {
  if (activeStep > 0) {
    activeStep -= 1;
    renderStep();
  }
});

nextButton?.addEventListener('click', () => {
  const current = steps[activeStep];
  const required = current.querySelectorAll('[required]');
  const allValid = Array.from(required).every((input) => input.value.trim() !== '');
  if (!allValid) {
    alert('Please complete required fields before continuing.');
    return;
  }
  if (activeStep < steps.length - 1) {
    activeStep += 1;
    renderStep();
  }
});

renderStep();
