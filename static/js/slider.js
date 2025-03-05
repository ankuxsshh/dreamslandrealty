function initializeRangeSliders(country) {
  const priceDisplay = document.getElementById("price-display");
  const sqftDisplay = document.getElementById("sqft-display");
  const minPrice = document.getElementById("min-price");
  const maxPrice = document.getElementById("max-price");
  const minSqft = document.getElementById("min-sqft");
  const maxSqft = document.getElementById("max-sqft");

  // Format currency based on country
  const formatCurrency = (value, country) => {
    const currency = country === "dubai" ? "AED" : "INR";
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
    }).format(value);
  };

  // Update Price Range Display
  function updatePriceDisplay() {
    const min = parseInt(minPrice.value, 10);
    const max = parseInt(maxPrice.value, 10);

    if (min > max) minPrice.value = max;
    priceDisplay.textContent = `${formatCurrency(minPrice.value, country)} - ${formatCurrency(maxPrice.value, country)}`;
  }

  // Update Square Footage Display
  function updateSqftDisplay() {
    const min = parseInt(minSqft.value, 10);
    const max = parseInt(maxSqft.value, 10);

    if (min > max) minSqft.value = max;
    sqftDisplay.textContent = `${minSqft.value} - ${maxSqft.value} sqft`;
  }

  // Attach events to sliders
  minPrice.addEventListener("input", updatePriceDisplay);
  maxPrice.addEventListener("input", updatePriceDisplay);

  minSqft.addEventListener("input", updateSqftDisplay);
  maxSqft.addEventListener("input", updateSqftDisplay);

  // Reset sliders on Clear
  document.getElementById("clear-filter").addEventListener("click", () => {
    minPrice.value = minPrice.min;
    maxPrice.value = maxPrice.max;
    minSqft.value = minSqft.min;
    maxSqft.value = maxSqft.max;
    updatePriceDisplay();
    updateSqftDisplay();
  });

  // Initialize displays
  updatePriceDisplay();
  updateSqftDisplay();
}

// Initialize the sliders on page load
const country = "india"; // Or dynamically set it
initializeRangeSliders(country);
