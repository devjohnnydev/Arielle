// Dashboard JavaScript for Chart.js initialization and interactions

/**
 * Initialize dashboard charts with provided data
 * @param {Array} sizeData - Array of size distribution data
 * @param {Array} congregationData - Array of congregation data
 */
function initializeDashboardCharts(sizeData, congregationData) {
    // Initialize size distribution chart (doughnut chart)
    initializeSizeChart(sizeData);
    
    // Initialize congregation distribution chart (bar chart)
    initializeCongregationChart(congregationData);
    
    // Initialize any additional interactive features
    initializeDashboardInteractions();
}

/**
 * Initialize the size distribution doughnut chart
 * @param {Array} sizeData - Size distribution data
 */
function initializeSizeChart(sizeData) {
    const ctx = document.getElementById('sizeChart');
    if (!ctx) return;
    
    const chartColors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ];
    
    new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: sizeData.map(item => item.size),
            datasets: [{
                data: sizeData.map(item => item.quantity),
                backgroundColor: chartColors.slice(0, sizeData.length),
                borderColor: '#fff',
                borderWidth: 2,
                hoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

/**
 * Initialize the congregation distribution bar chart
 * @param {Array} congregationData - Congregation data
 */
function initializeCongregationChart(congregationData) {
    const ctx = document.getElementById('congregationChart');
    if (!ctx) return;
    
    new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: congregationData.map(item => {
                // Truncate long congregation names for better display
                return item.congregation.length > 20 
                    ? item.congregation.substring(0, 17) + '...'
                    : item.congregation;
            }),
            datasets: [{
                label: 'Quantidade',
                data: congregationData.map(item => item.quantity),
                backgroundColor: 'rgba(44, 82, 130, 0.8)',
                borderColor: 'rgba(44, 82, 130, 1)',
                borderWidth: 1,
                borderRadius: 4,
                hoverBackgroundColor: 'rgba(44, 82, 130, 0.9)',
                hoverBorderColor: 'rgba(44, 82, 130, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 0,
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            const index = context[0].dataIndex;
                            return congregationData[index].congregation;
                        },
                        label: function(context) {
                            const index = context.dataIndex;
                            const data = congregationData[index];
                            return [
                                `Quantidade: ${data.quantity}`,
                                `Valor: R$ ${data.amount.toFixed(2)}`
                            ];
                        }
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

/**
 * Initialize dashboard interactions and features
 */
function initializeDashboardInteractions() {
    // Add click handlers for KPI cards
    initializeKpiCardInteractions();
    
    // Initialize any tooltips
    initializeTooltips();
    
    // Initialize auto-refresh functionality if needed
    initializeAutoRefresh();
    
    // Add keyboard shortcuts
    initializeKeyboardShortcuts();
}

/**
 * Initialize KPI card click interactions
 */
function initializeKpiCardInteractions() {
    const kpiCards = document.querySelectorAll('.card.bg-primary, .card.bg-success, .card.bg-warning, .card.bg-info');
    
    kpiCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            // Add a subtle animation on click
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
            
            // You can add navigation logic here based on the card type
            // For example, redirect to orders page with specific filters
        });
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize auto-refresh functionality (optional)
 */
function initializeAutoRefresh() {
    // This could be used to periodically refresh dashboard data
    // For now, we'll just log that it's initialized
    console.log('Auto-refresh initialized (currently disabled)');
    
    // Example implementation:
    // setInterval(() => {
    //     refreshDashboardData();
    // }, 300000); // Refresh every 5 minutes
}

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
        // Alt + N = New Order
        if (event.altKey && event.key.toLowerCase() === 'n') {
            event.preventDefault();
            window.location.href = '/orders/add';
        }
        
        // Alt + O = Orders page
        if (event.altKey && event.key.toLowerCase() === 'o') {
            event.preventDefault();
            window.location.href = '/orders';
        }
        
        // Alt + R = Reports page
        if (event.altKey && event.key.toLowerCase() === 'r') {
            event.preventDefault();
            window.location.href = '/reports';
        }
        
        // Alt + D = Dashboard
        if (event.altKey && event.key.toLowerCase() === 'd') {
            event.preventDefault();
            window.location.href = '/dashboard';
        }
    });
}

/**
 * Utility function to format currency
 * @param {number} value - Numeric value to format
 * @returns {string} Formatted currency string
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Utility function to format percentage
 * @param {number} value - Numeric value to format as percentage
 * @returns {string} Formatted percentage string
 */
function formatPercentage(value) {
    return `${value.toFixed(1)}%`;
}

/**
 * Function to refresh dashboard data (can be called externally)
 */
function refreshDashboardData() {
    console.log('Refreshing dashboard data...');
    // This would typically make an AJAX call to refresh data
    // For now, we'll just reload the page
    window.location.reload();
}

/**
 * Initialize dashboard when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add hover effects to tables
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(4px)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
    
    console.log('Dashboard JavaScript initialized');
});

// Export functions for potential external use
window.dashboardUtils = {
    initializeDashboardCharts,
    formatCurrency,
    formatPercentage,
    refreshDashboardData
};
