
document.addEventListener("DOMContentLoaded", function() {
    GreenAudioPlayer.init({
        selector: ".player-original",
        stopOthersOnPlay: true,
        showTooltips: true,
        showDownloadButton: true,
        enableKeystrokes: true
    });

    GreenAudioPlayer.init({
        selector: ".player-result",
        stopOthersOnPlay: true,
        showTooltips: true,
        showDownloadButton: true,
        enableKeystrokes: true
    });
});
