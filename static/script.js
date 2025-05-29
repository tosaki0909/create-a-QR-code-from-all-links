document.addEventListener("DOMContentLoaded", function () {
    // Validasi input URL secara real-time
    document.getElementById("url-input").addEventListener("input", function () {
        let url = this.value;
        let regex = /^(https?:\/\/)?([\w\d-]+\.)+[\w-]{2,}(\/.*)?$/;
        document.getElementById("url-error").style.display = regex.test(url) ? "none" : "block";
    });

    // Animasi loading saat submit
    document.getElementById("qr-form").addEventListener("submit", function () {
        document.getElementById("loading").style.display = "block";
    });

    // Mode gelap dengan penyimpanan preferensi pengguna
    const toggleThemeBtn = document.getElementById("toggle-theme");
    toggleThemeBtn.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");
    });

    // Salin link QR Code
    function copyQRLink() {
        let qrImg = document.querySelector(".qr-container img");
        if (qrImg) {
            navigator.clipboard.writeText(qrImg.src);
            alert("Link QR Code telah disalin!");
        } else {
            alert("QR Code tidak ditemukan!");
        }
    }
});