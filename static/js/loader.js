// Hide loader after page load and show buttons
window.addEventListener('load', function () {
    const loader = document.getElementById('loader');
    const fixedButtons = document.querySelectorAll('.fixed-buttons'); // Select all fixed buttons

    if (loader) {
        loader.classList.add('hidden');
    }

    if (fixedButtons) {
        fixedButtons.forEach(button => {
            button.style.visibility = 'visible'; // Make sure buttons are visible after the loader disappears
        });
    }
});
