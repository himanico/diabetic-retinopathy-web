const imageInput = document.querySelector('input[name="image"]');

if (imageInput) {
    imageInput.addEventListener('change', function () {
        if (this.files.length > 0) {
            console.log("Image selected: " + this.files[0].name);
        }
    });
}