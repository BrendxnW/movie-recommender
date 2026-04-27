
document.addEventListener('DOMContentLoaded', function() {
    const remixForm = document.getElementById('remix-form');
    const loadingOverlay = document.getElementById('loading-overlay');

    if (remixForm && loadingOverlay) {
    remixForm.addEventListener('submit', function(e) {
        const submitter = e.submitter || document.activeElement;
        if (submitter && submitter.name === 'action' && submitter.value === 'submit_remix') {
        loadingOverlay.classList.remove('hidden');
        }
    });
    }
});