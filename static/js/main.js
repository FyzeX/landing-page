// Main JavaScript file for Telegram Market Bot

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        });
    }, 5000);

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Template card hover effects
    const templateCards = document.querySelectorAll('.template-card');
    templateCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Demo bot generation
    const demoButtons = document.querySelectorAll('.demo-btn');
    demoButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const templateId = this.dataset.templateId;
            generateDemo(templateId, this);
        });
    });

    // Purchase buttons
    const purchaseButtons = document.querySelectorAll('.purchase-btn');
    purchaseButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!isUserLoggedIn()) {
                e.preventDefault();
                showLoginModal();
            }
        });
    });

    // Filter functionality
    initializeFilters();
    
    // Search functionality
    initializeSearch();
});

// Demo bot generation function
function generateDemo(templateId, button) {
    const originalText = button.innerHTML;
    const originalDisabled = button.disabled;
    
    // Show loading state
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    button.disabled = true;
    
    const formData = new FormData();
    formData.append('template_id', templateId);
    formData.append('csrfmiddlewaretoken', getCsrfToken());
    
    fetch('/demo-bot/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showDemoModal(data);
        } else {
            showAlert('error', data.error || 'Failed to generate demo bot');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('error', 'An error occurred while generating the demo bot');
    })
    .finally(() => {
        // Restore button state
        button.innerHTML = originalText;
        button.disabled = originalDisabled;
    });
}

// Show demo modal
function showDemoModal(data) {
    const modal = document.getElementById('demoModal');
    if (modal) {
        document.getElementById('demoBotUsername').textContent = data.bot_username;
        document.getElementById('demoExpiresAt').textContent = data.expires_at;
        document.getElementById('telegramLink').href = data.demo_url;
        
        // Show features and commands
        const featuresList = document.getElementById('demoFeatures');
        const commandsList = document.getElementById('demoCommands');
        
        if (featuresList && data.features) {
            featuresList.innerHTML = data.features.map(feature => `<li>${feature}</li>`).join('');
        }
        
        if (commandsList && data.commands) {
            commandsList.innerHTML = data.commands.map(command => `<li><code>${command}</code></li>`).join('');
        }
        
        new bootstrap.Modal(modal).show();
    }
}

// Filter initialization
function initializeFilters() {
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        const inputs = filterForm.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }
}

// Search initialization
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const query = this.value.trim();
                if (query.length >= 3 || query.length === 0) {
                    performSearch(query);
                }
            }, 500);
        });
    }
}

// Perform search
function performSearch(query) {
    const url = new URL(window.location);
    if (query) {
        url.searchParams.set('search', query);
    } else {
        url.searchParams.delete('search');
    }
    window.location.href = url.toString();
}

// Utility functions
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

function isUserLoggedIn() {
    return document.body.dataset.userAuthenticated === 'true';
}

function showLoginModal() {
    const loginUrl = '/users/login/';
    window.location.href = `${loginUrl}?next=${encodeURIComponent(window.location.pathname)}`;
}

function showAlert(type, message) {
    const alertContainer = document.getElementById('alertContainer') || document.querySelector('.container');
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show`;
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    if (alertContainer) {
        alertContainer.insertBefore(alertElement, alertContainer.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            alertElement.remove();
        }, 5000);
    }
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('success', 'Copied to clipboard!');
    }).catch(() => {
        showAlert('error', 'Failed to copy to clipboard');
    });
}

// Format price
function formatPrice(price, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(price);
}

// Countdown timer
function startCountdown(elementId, targetDate) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const timer = setInterval(() => {
        const now = new Date().getTime();
        const target = new Date(targetDate).getTime();
        const distance = target - now;
        
        if (distance < 0) {
            clearInterval(timer);
            element.innerHTML = 'EXPIRED';
            return;
        }
        
        const hours = Math.floor(distance / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        element.innerHTML = `${hours}h ${minutes}m ${seconds}s`;
    }, 1000);
}

// Loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'spinner-overlay';
    overlay.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.querySelector('.spinner-overlay');
    if (overlay) {
        overlay.remove();
    }
}