const carousel = document.getElementById('carousel');
const nextBtn = document.getElementById('next');
const prevBtn = document.getElementById('prev');

let index = 0;
let direction = 1; // 1 = adelante, -1 = atrás
const slides = carousel.children;
const totalSlides = slides.length;

function showSlide(i) {
    carousel.style.transform = `translateX(-${i * 100}%)`;
}

// Función para moverse automáticamente tipo ping-pong
function autoSlide() {
    index += direction;

    // Cambiar dirección si llegamos a los extremos
    if(index >= totalSlides - 1 || index <= 0) {
        direction *= -1;
    }

    showSlide(index);
}

// Botones
nextBtn.addEventListener('click', () => {
    direction = 1;
    index = (index + 1) % totalSlides;
    showSlide(index);
});

prevBtn.addEventListener('click', () => {
    direction = -1;
    index = (index - 1 + totalSlides) % totalSlides;
    showSlide(index);
});

// Autoplay cada 4s
setInterval(autoSlide, 4000);