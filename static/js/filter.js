document.addEventListener("DOMContentLoaded", () => {
  // Button Elements for Country Selection
  const countryButtons = {
    dubai: document.getElementById("btn-dubai"),
    india: document.getElementById("btn-india"),
  };

  // Input Elements for Filters
  const locationInput = document.getElementById("locationSearch");
  const propertyTypeSelect = document.getElementById("property-type");
  const subtypeSelect = document.getElementById("property-subtype");
  const sqftRangeDiv = document.getElementById("sqft-range");
  const bhkDiv = document.getElementById("bhk-options");
  const priceDisplay = document.getElementById("price-display");
  const sqftDisplay = document.getElementById("sqft-display");
  const minPriceInput = document.getElementById("min-price");
  const maxPriceInput = document.getElementById("max-price");
  const minSqftInput = document.getElementById("min-sqft");
  const maxSqftInput = document.getElementById("max-sqft");
  const filterForm = document.getElementById("filter-form");
  const clearFilterButton = document.getElementById("clear-filter");
  const conditionalFiltersDiv = document.getElementById("conditional-filters");

  let country = "india"; // Default country for the filters

  // Section: Update Property Type Options
  const updatePropertyTypes = () => {
    if (country === "dubai") {
      propertyTypeSelect.innerHTML = `
        <option value="" disabled selected>-Select-</option>
        <option value="residential">Residential</option>
      `;
    } else {
      propertyTypeSelect.innerHTML = `
        <option value="" disabled selected>-Select-</option>
        <option value="residential">Residential</option>
        <option value="commercial">Commercial</option>
      `;
    }
  };

  // Section: Update Subproperty Types Based on Property Type
  const updateSubtypes = () => {
    const selectedType = propertyTypeSelect.value;

    if (selectedType === "residential") {
      // Residential subtypes
      subtypeSelect.innerHTML = `
        <option value="" disabled selected>-Select Subtype-</option>
        <option value="residential_apartments">Residential Apartment</option>
        <option value="residential_villas/houses">Residential Villa/ House</option>
        <option value="residential_land">Residential Land</option>
        <option value="residential_others">Residential Other</option>
      `;
      conditionalFiltersDiv.style.display = "block";
      bhkDiv.style.display = "flex"; // Show BHK options for residential properties
      sqftRangeDiv.style.display = "block"; // Show Sqft for default residential subtypes
    } else if (selectedType === "commercial") {
      subtypeSelect.innerHTML = `
        <option value="" disabled selected>-Select Subtype-</option>
        <option value="commercial_shop">Commercial Shop</option>
        <option value="commercial_land">Commercial Land</option>
        <option value="commercial_building">Commercial Building</option>
        <option value="commercial_others">Commercial Other</option>
      `;
      conditionalFiltersDiv.style.display = "block";
      sqftRangeDiv.style.display = "block"; // Show Sqft range for commercial subtypes
      bhkDiv.style.display = "none"; // Hide BHK options for commercial properties
    } else {
      conditionalFiltersDiv.style.display = "none";
    }

    document.getElementById("property-subtypes").style.display = "block";
  };

  // Section: Handle Subtype-Specific Display Logic
  const handleSubtypeSpecificFilters = () => {
    const selectedSubtype = subtypeSelect.value;

    // Check for Residential Land
    if (selectedSubtype === "residential_land") {
      sqftRangeDiv.style.display = "none"; // Hide Sqft Range for Residential Land
      bhkDiv.style.display = "none"; // Hide BHK options for Residential Land
      const checkboxes = document.getElementsByClassName('btn-check');
      for (let i = 0; i < checkboxes.length; i++) {
          checkboxes[i].checked = false;
    }
    } else if (propertyTypeSelect.value === "commercial") {
      bhkDiv.style.display = "none"; // Hide BHK options for any commercial subtype
      const checkboxes = document.getElementsByClassName('btn-check');
      for (let i = 0; i < checkboxes.length; i++) {
          checkboxes[i].checked = false;
    }
    } else {
      // Default behavior for other subtypes
      sqftRangeDiv.style.display = "block";
      bhkDiv.style.display = "flex";
    }
  };

  // Section: Reset All Filters
  const resetFilters = () => {
    locationInput.value = "";
    propertyTypeSelect.value = "";
    subtypeSelect.innerHTML = "";
    minPriceInput.value = 0;
    maxPriceInput.value = 10000000;
    minSqftInput.value = 500;
    maxSqftInput.value = 5000;
    bhkDiv.value = "";
    // bhk.value = "null";
    // Loop through all btn-check checkboxes and uncheck them
    const checkboxes = document.getElementsByClassName('btn-check');
    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = false;
    }
    priceDisplay.textContent = "0 - 10,000,000";
    sqftDisplay.textContent = "500 - 5000 sqft";
    // sqftDisplay.textContent = null;
    conditionalFiltersDiv.style.display = "none";
    sqftRangeDiv.style.display = "none";
    bhkDiv.style.display = "none";
    document.getElementById("property-subtypes").style.display = "none";
  };

  // Section: Update Price Display
  const updatePriceDisplay = () => {
    const minPrice = parseInt(minPriceInput.value, 10);
    const maxPrice = parseInt(maxPriceInput.value, 10);
    priceDisplay.textContent = `${minPrice.toLocaleString()} - ${maxPrice.toLocaleString()}`;
  };

  // Section: Update Sqft Display
  const updateSqftDisplay = () => {
    const minSqft = parseInt(minSqftInput.value, 10);
    const maxSqft = parseInt(maxSqftInput.value, 10);
    sqftDisplay.textContent = `${minSqft} - ${maxSqft} sqft`;
  };

  // Section: Event Listeners
  countryButtons.dubai.addEventListener("click", () => {
    country = "dubai";
    updatePropertyTypes();
    resetFilters();
  });

  countryButtons.india.addEventListener("click", () => {
    country = "india";
    updatePropertyTypes();
    resetFilters();
  });

  propertyTypeSelect.addEventListener("change", updateSubtypes);
  subtypeSelect.addEventListener("change", handleSubtypeSpecificFilters);

  minPriceInput.addEventListener("input", updatePriceDisplay);
  maxPriceInput.addEventListener("input", updatePriceDisplay);

  minSqftInput.addEventListener("input", updateSqftDisplay);
  maxSqftInput.addEventListener("input", updateSqftDisplay);

  clearFilterButton.addEventListener("click", resetFilters);

  filterForm.addEventListener("submit", (e) => {
    e.preventDefault(); // Prevent default submission
    
    // Prepare the form data to be sent for filtering
    const formData = {
      location: locationInput.value,
      property_type: propertyTypeSelect.value,
      property_subtype: subtypeSelect.value,
      min_price: minPriceInput.value,
      max_price: maxPriceInput.value,
      // min_sqft: minSqftInput.value,
      // max_sqft: maxSqftInput.value,
      // min_sqft: minSqftInput.value ? parseInt(minSqftInput.value, 10) : null,
      // max_sqft: maxSqftInput.value ? parseInt(minSqftInput.value, 10) : null,
      // bhk: document.querySelector('input[name="bhk"]:checked')?.value || -1,
    };

    // const selectedBhk = document.querySelector('input[name="bhk"]:checked');
    // if (selectedBhk) {
    //   formData.bhk = selectedBhk.value;
    // }

    if (subtypeSelect.value !== 'residential_land') {
      formData.min_sqft = minSqftInput.value;
      formData.max_sqft = maxSqftInput.value;
      formData.bhk = document.querySelector('input[name="bhk"]:checked')?.value
    } 

    // Dynamically generate the query string for the filter form
    const queryString = new URLSearchParams(formData).toString();

    // Redirect to the properties list page with the filters applied
    window.location.href = `/propertieslist/?${queryString}`;
  });

  // Section: Initialize Property Filters
  updatePropertyTypes();
});
