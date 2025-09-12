// js/sliders.js

function updateSliderBackground(slider) {
    const value = slider.value;
    const min = slider.min ? slider.min : 0;
    const max = slider.max ? slider.max : 100;
    const percentage = ((value - min) * 100) / (max - min);

    slider.style.background = `linear-gradient(to right, #2980b9 0%, #2980b9 ${percentage}%, #dfe6e9 ${percentage}%, #dfe6e9 100%)`;
}

document.addEventListener('DOMContentLoaded', () => {
    const sliders = document.querySelectorAll('input[type="range"]');

    sliders.forEach(slider => {
        // Mise à jour initiale
        updateSliderBackground(slider);

        // Mise à jour à chaque changement
        slider.addEventListener('input', () => {
            updateSliderBackground(slider);
        });
    });
});
