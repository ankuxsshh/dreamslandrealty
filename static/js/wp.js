function sendToWhatsApp(property_id) {
    let url = `https://dreamslandrealty.com/send_whatsapp/?property_id=${encodeURIComponent(property_id)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.whatsapp_url;
            } else {
                alert("Failed to generate WhatsApp link.");
            }
        })
        .catch(error => console.error("Error:", error));
}