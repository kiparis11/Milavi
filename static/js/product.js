document.addEventListener('DOMContentLoaded', function () {
    const priceElement = document.querySelector('#product-price');

    if (!priceElement) {
        return;
    }

    const sizeButtons = document.querySelectorAll('.product-size');
    const temperatureButtons = document.querySelectorAll('.product-temperature');
    const addonInputs = document.querySelectorAll('.product-addon__input');

    const selectedSizeInput = document.querySelector('#selected-size');
    const selectedTemperatureInput = document.querySelector('#selected-temperature');

    const basePrice = Number(priceElement.dataset.basePrice);


    function formatPrice(price) {
        return new Intl.NumberFormat('ru-RU').format(price) + ' сум';
    }


    function updatePrice() {
        let finalPrice = basePrice;

        const activeSize = document.querySelector(
            '.product-size--active'
        );

        if (activeSize) {
            finalPrice += Number(activeSize.dataset.extra);
        }


        addonInputs.forEach(function (addon) {
            if (addon.checked) {
                finalPrice += Number(addon.dataset.extra);
            }
        });


        priceElement.textContent = formatPrice(finalPrice);
    }


    /* Размер */

    sizeButtons.forEach(function (button) {
        button.addEventListener('click', function () {

            sizeButtons.forEach(function (item) {
                item.classList.remove('product-size--active');
            });

            button.classList.add('product-size--active');

            if (selectedSizeInput) {
                selectedSizeInput.value = button.dataset.sizeId;
            }

            updatePrice();
        });
    });


    /* Ставим первый размер по умолчанию */

    const activeSize = document.querySelector(
        '.product-size--active'
    );

    if (activeSize && selectedSizeInput) {
        selectedSizeInput.value = activeSize.dataset.sizeId;
    }


    /* Температура */

    temperatureButtons.forEach(function (button) {
        button.addEventListener('click', function () {

            temperatureButtons.forEach(function (item) {
                item.classList.remove(
                    'product-temperature--active'
                );
            });

            button.classList.add(
                'product-temperature--active'
            );

            if (selectedTemperatureInput) {
                selectedTemperatureInput.value =
                    button.dataset.temperature;
            }
        });
    });


    /* Добавки */

    addonInputs.forEach(function (addon) {
        addon.addEventListener('change', function () {
            updatePrice();
        });
    });


    updatePrice();
});