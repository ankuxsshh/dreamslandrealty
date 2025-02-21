document.addEventListener('DOMContentLoaded', () => {
    // Try to select elements with error handling
    const locationBtn = document.querySelector('.location-btn');
    const barsBtn = document.querySelector('.bars-btn');
    const locationOverlay = document.querySelector('.location-overlay');
    const filterOverlay = document.querySelector('.filter-overlay');
    const closeFilterBtn = document.getElementById('clear-filter');
    const locationContainer = document.querySelector('.location-container');
    const filterContainer = document.querySelector('.filter-container');

    // List of required elements
    const requiredElements = [
        { name: 'locationBtn', element: locationBtn },
        { name: 'barsBtn', element: barsBtn },
        { name: 'locationOverlay', element: locationOverlay },
        { name: 'filterOverlay', element: filterOverlay },
        { name: 'closeFilterBtn', element: closeFilterBtn },
        { name: 'locationContainer', element: locationContainer },
        { name: 'filterContainer', element: filterContainer }
    ];

    // Check for missing elements and log a warning
    const missingElements = requiredElements.filter(item => !item.element);

    if (missingElements.length > 0) {
        // Log a warning for each missing element
        missingElements.forEach(item => {
            console.warn(`Missing required element: ${item.name}`);
        });
    } else {
        // All elements are present, proceed with adding event listeners

        // Function to toggle overlays and containers
        function toggleOverlay(overlay, container) {
            overlay.classList.toggle('active');
            container.classList.toggle('active');
        }

        // Function to close overlays and containers
        function closeOverlay(overlay, container) {
            overlay.classList.remove('active');
            container.classList.remove('active');
        }

        // Add event listeners for opening overlays
        if (locationBtn) {
            locationBtn.addEventListener('click', () => toggleOverlay(locationOverlay, locationContainer));
        }
        if (barsBtn) {
            barsBtn.addEventListener('click', () => toggleOverlay(filterOverlay, filterContainer));
        }

        // Close Filter when 'Clear' button is clicked
        if (closeFilterBtn) {
            closeFilterBtn.addEventListener('click', () => closeOverlay(filterOverlay, filterContainer));
        }

        // Close Location Overlay on clicking the overlay
        if (locationOverlay) {
            locationOverlay.addEventListener('click', (event) => {
                if (event.target === locationOverlay) closeOverlay(locationOverlay, locationContainer);
            });
        }

        // Close Filter Overlay on clicking the overlay
        if (filterOverlay) {
            filterOverlay.addEventListener('click', (event) => {
                if (event.target === filterOverlay) closeOverlay(filterOverlay, filterContainer);
            });
        }
    }
});
