document.addEventListener('DOMContentLoaded', function () {
    const slider = document.querySelector('.hero-slider');

    if (!slider) {
        return;
    }

    const slides = slider.querySelectorAll('.hero-slide');
    const dots = slider.querySelectorAll('.hero-slider__dot');
    const prevButton = slider.querySelector('.hero-slider__arrow--prev');
    const nextButton = slider.querySelector('.hero-slider__arrow--next');

    let currentSlide = 0;
    let autoSlide;


    function showSlide(index) {
        if (index >= slides.length) {
            index = 0;
        }

        if (index < 0) {
            index = slides.length - 1;
        }

        slides.forEach(function (slide) {
            slide.classList.remove('hero-slide--active');
        });

        dots.forEach(function (dot) {
            dot.classList.remove('hero-slider__dot--active');
        });

        slides[index].classList.add('hero-slide--active');
        dots[index].classList.add('hero-slider__dot--active');

        currentSlide = index;
    }


    function nextSlide() {
        showSlide(currentSlide + 1);
    }


    function prevSlide() {
        showSlide(currentSlide - 1);
    }


    nextButton.addEventListener('click', nextSlide);
    prevButton.addEventListener('click', prevSlide);


    dots.forEach(function (dot, index) {
        dot.addEventListener('click', function () {
            showSlide(index);
        });
    });


    function startAutoSlide() {
        autoSlide = setInterval(nextSlide, 6000);
    }


    function stopAutoSlide() {
        clearInterval(autoSlide);
    }


    slider.addEventListener('mouseenter', stopAutoSlide);
    slider.addEventListener('mouseleave', startAutoSlide);


    showSlide(0);
    startAutoSlide();
});