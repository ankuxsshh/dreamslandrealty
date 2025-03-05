// document.addEventListener('DOMContentLoaded', function() {
//     const propertyTypeField = document.querySelector('#id_property_type');
//     const propertySubtypeField = document.querySelector('#id_property_subtype');
//     const bhkField = document.querySelector('.form-row.field-bhk');
//     const squareFeetField = document.querySelector('.form-row.field-square_feet');

//     function toggleFields() {
//         const propertyType = propertyTypeField ? propertyTypeField.value : '';
//         const propertySubtype = propertySubtypeField ? propertySubtypeField.value : '';

//         if (propertyType === 'residential' && propertySubtype === 'residential_land') {
//             bhkField.style.display = 'none';
//             squareFeetField.style.display = 'none';
//         } else {
//             bhkField.style.display = '';
//             squareFeetField.style.display = '';
//         }
//     }

//     if (propertyTypeField && propertySubtypeField) {
//         propertyTypeField.addEventListener('change', toggleFields);
//         propertySubtypeField.addEventListener('change', toggleFields);
//         toggleFields();  // Initial check when page loads
//     }
// });



// console.log("Property form script loaded!");
