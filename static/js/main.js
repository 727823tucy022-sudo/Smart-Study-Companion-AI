// Generic Application Utility and User Experience Methods
function showToastNotification(message, contextualType = 'success') {
    const container = document.getElementById('toast-mount-wrapper');
    if (!container) return;

    const toastElement = document.createElement('div');
    toastElement.className = `toast align-items-center text-white bg-${contextualType} border-0 shadow-lg mb-2`;
    toastElement.role = 'alert';
    toastElement.ariaLive = 'assertive';
    toastElement.ariaAtomic = 'true';

    toastElement.innerHTML = `
        <div class="d-flex">
            <div class="toast-body font-weight-bold">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    container.appendChild(toastElement);
    const bsToast = new bootstrap.Toast(toastElement, { delay: 4000 });
    bsToast.show();

    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Active link highlighting indicator configuration
document.addEventListener('DOMContentLoaded', () => {
    const currentRoutePath = window.location.pathname;
    const links = document.querySelectorAll('.navbar-nav .nav-link');
    links.forEach(link => {
        if (link.getAttribute('href') === currentRoutePath) {
            link.classList.add('active');
        }
    });
});