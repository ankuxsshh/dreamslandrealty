document.getElementById('contact-form').addEventListener('submit', function (event) {
  event.preventDefault(); // Prevent form submission

  const phone = document.getElementById('phone').value;
  const fullname = document.getElementById('fullname').value;
  const listingtype = document.getElementById('listingtype').value;
  const address = document.getElementById('address').value;

  const message = `Name: ${fullname}\nPhone: ${phone}\nListing Type: ${listingtype}\nAddress/Comments: ${address}`;
  const whatsappLink = `https://wa.me/+916238061066?text=${encodeURIComponent(message)}`;

  window.open(whatsappLink, '_blank'); // Open WhatsApp with the message
});