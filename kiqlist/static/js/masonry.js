var renderMasonryEvent = new CustomEvent('kiqlistRenderMasonry', {
    bubbles: true,
    cancelable: false
});

function renderMasonry(element) {
    $(element).imagesLoaded(function () {
        $(element).masonry({
            itemSelector: '.goal-card, .profile-holder, .dashboard-holder',
            isFitWidth: false
        });
    });
}

function renderMasonryHandler() {
    renderMasonry(this);
}