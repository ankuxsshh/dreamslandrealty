let images = []
let currentIndex = 0

document.querySelectorAll('.preview-image').forEach((img, index) => {
    images.push(img.src)
    img.addEventListener('click', function () {
        openOverlay(index)
    })
})

function openOverlay(index) {
    currentIndex = index
    document.getElementById('fullscreen-img').src = images[currentIndex]
    document.getElementById('fullscreen-overlay').style.display = 'flex'
}

function closeOverlay() {
    document.getElementById('fullscreen-overlay').style.display = 'none'
}

function changeImage(direction) {
    currentIndex += direction
    if (currentIndex < 0) {
        currentIndex = images.length - 1
    } else if (currentIndex >= images.length) {
        currentIndex = 0
    }
    document.getElementById('fullscreen-img').src = images[currentIndex]
}