// Add active class to current nav item
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath) {
            link.classList.add('active');
        }
    });
});

// Toast Notification System
function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let iconClass = 'fas fa-info-circle';
    if (type === 'success') iconClass = 'fas fa-check-circle';
    if (type === 'error') iconClass = 'fas fa-exclamation-circle';
    if (type === 'warning') iconClass = 'fas fa-exclamation-triangle';

    toast.innerHTML = `
        <i class="${iconClass}"></i>
        <div class="toast-message">${message}</div>
    `;

    container.appendChild(toast);

    // Auto remove after animation ends (5s total: 4.5s delay + 0.5s fadeOut)
    setTimeout(() => {
        toast.remove();
    }, 5000);
}
