/**
 * EvoTransformer Dashboard JavaScript
 * Handles data fetching, chart rendering, and real-time updates
 */

// Global variables
let socket;
let charts = {};

// Chart color scheme
const colors = {
    primary: '#667eea',
    secondary: '#764ba2',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#3b82f6',
    gray: '#6b7280'
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Initializing EvoTransformer Dashboard...');

    try {
        // Load all metrics
        await loadAllMetrics();

        // Initialize WebSocket connection
        initializeWebSocket();

        // Set up auto-refresh
        setInterval(() => updateLastUpdated(), 60000); // Update every minute

        console.log('✅ Dashboard initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing dashboard:', error);
    }
});

// Load all metrics from API
async function loadAllMetrics() {
    try {
        const response = await fetch('/api/all-metrics');
        const data = await response.json();

        // Update overview cards
        updateOverviewCards(data.overview);

        // Render charts
        renderTrainingChart(data.training_progress);
        renderComparisonChart(data.competitive_comparison);
        renderFeatureImpactChart(data.feature_impact);

        // Update architecture details
        updateArchitectureDetails(data.architecture);

        // Update resource details
        updateResourceDetails(data.resources);

        // Render roadmap
        renderRoadmap(data.roadmap);

    } catch (error) {
        console.error('Error loading metrics:', error);
    }
}

// Update overview cards
function updateOverviewCards(overview) {
    // Current accuracy
    const accuracyElement = document.getElementById('currentAccuracy');
    if (accuracyElement) {
        accuracyElement.textContent = `${overview.current_accuracy.toFixed(2)}%`;
        animateValue(accuracyElement, 0, overview.current_accuracy, 1500, '%');
    }

    // Accuracy change
    const changeElement = document.getElementById('accuracyChange');
    if (changeElement) {
        changeElement.textContent = `+${overview.improvement.toFixed(2)}% vs baseline`;
    }

    // Confidence interval
    const confidenceElement = document.getElementById('confidence');
    if (confidenceElement) {
        confidenceElement.textContent = '95%';
    }
}

// Update architecture details
function updateArchitectureDetails(architecture) {
    const updates = {
        'baseModel': architecture.base_model,
        'evolvedLayers': architecture.num_evolved_layers,
        'attentionHeads': architecture.num_attention_heads,
        'hiddenDim': architecture.hidden_dim,
        'ffnDim': architecture.ffn_dim,
        'dropout': architecture.dropout
    };

    Object.entries(updates).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) element.textContent = value;
    });
}

// Update resource details
function updateResourceDetails(resources) {
    const updates = {
        'gpu': resources.gpu,
        'vram': resources.vram,
        'batchSize': resources.batch_size,
        'lrRoberta': resources.learning_rate_roberta,
        'lrEvolved': resources.learning_rate_evolved,
        'framework': resources.framework
    };

    Object.entries(updates).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) element.textContent = value;
    });
}

// Render training progress chart
function renderTrainingChart(trainingData) {
    const ctx = document.getElementById('trainingChart');
    if (!ctx) return;

    // Destroy existing chart if it exists
    if (charts.training) {
        charts.training.destroy();
    }

    const epochs = trainingData.map(d => `Epoch ${d.epoch}`);
    const accuracies = trainingData.map(d => d.accuracy);
    const losses = trainingData.map(d => d.loss);

    charts.training = new Chart(ctx, {
        type: 'line',
        data: {
            labels: epochs,
            datasets: [
                {
                    label: 'Validation Accuracy',
                    data: accuracies,
                    borderColor: colors.primary,
                    backgroundColor: `${colors.primary}20`,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                },
                {
                    label: 'Loss',
                    data: losses,
                    borderColor: colors.danger,
                    backgroundColor: `${colors.danger}20`,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: colors.danger,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: '600'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += context.datasetIndex === 0
                                    ? context.parsed.y.toFixed(2) + '%'
                                    : context.parsed.y.toFixed(3);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Accuracy (%)',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Loss',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Render model comparison chart (bubble chart)
function renderComparisonChart(comparisonData) {
    const ctx = document.getElementById('comparisonChart');
    if (!ctx) return;

    if (charts.comparison) {
        charts.comparison.destroy();
    }

    // Prepare bubble data: x=parameters, y=accuracy, r=efficiency
    const bubbleData = comparisonData.map((model, index) => ({
        x: model.parameters,
        y: model.accuracy,
        r: Math.max(model.efficiency * 5, 8), // Scale radius
        label: model.model
    }));

    // Color mapping
    const colorMap = {
        'Current Best': colors.primary,
        'SOTA Target': colors.success,
        'Baseline': colors.warning,
        'Legacy': colors.gray,
        'Industry Leader': colors.secondary
    };

    const datasets = bubbleData.map((point, index) => ({
        label: point.label,
        data: [point],
        backgroundColor: `${colorMap[comparisonData[index].status] || colors.info}80`,
        borderColor: colorMap[comparisonData[index].status] || colors.info,
        borderWidth: 2
    }));

    charts.comparison = new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 10,
                        font: {
                            size: 11,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const model = comparisonData[context.datasetIndex];
                            return [
                                `Accuracy: ${model.accuracy.toFixed(2)}%`,
                                `Parameters: ${model.parameters}M`,
                                `Efficiency: ${model.efficiency.toFixed(2)}%/M`
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Accuracy (%)',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    min: 50,
                    max: 80,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Parameters (Millions)',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    type: 'logarithmic',
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        }
    });
}

// Render feature impact chart
function renderFeatureImpactChart(featureData) {
    const ctx = document.getElementById('featureImpactChart');
    if (!ctx) return;

    if (charts.featureImpact) {
        charts.featureImpact.destroy();
    }

    const features = featureData.map(f => f.feature);
    const impacts = featureData.map(f => f.impact);

    charts.featureImpact = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: features,
            datasets: [{
                label: 'Impact (%)',
                data: impacts,
                backgroundColor: [
                    `${colors.primary}`,
                    `${colors.secondary}`,
                    `${colors.success}`,
                    `${colors.info}`,
                    `${colors.warning}`
                ],
                borderRadius: 8,
                borderWidth: 0
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const feature = featureData[context.dataIndex];
                            return [
                                `Impact: +${feature.impact}%`,
                                feature.description
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Accuracy Improvement (%)',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    beginAtZero: true
                },
                y: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Render roadmap items
function renderRoadmap(roadmapData) {
    const container = document.getElementById('roadmapGrid');
    if (!container) return;

    container.innerHTML = roadmapData.map(item => `
        <div class="roadmap-item ${item.status}">
            <div class="roadmap-header">
                <h4 class="roadmap-title">${item.enhancement}</h4>
                <span class="roadmap-badge ${item.status}">${item.status}</span>
            </div>
            <div class="roadmap-gain">+${item.expected_gain.toFixed(1)}%</div>
            <p class="roadmap-note">${item.note}</p>
        </div>
    `).join('');
}

// Initialize WebSocket for real-time updates
function initializeWebSocket() {
    try {
        socket = io();

        socket.on('connect', () => {
            console.log('✅ WebSocket connected');
        });

        socket.on('connection_response', (data) => {
            console.log('📡', data.message);
        });

        socket.on('live_metrics_update', (data) => {
            console.log('📊 Received live metrics update');
            updateOverviewCards(data);
        });

        socket.on('training_update', (data) => {
            console.log('🔄 Training update:', data.message);
        });

        socket.on('disconnect', () => {
            console.log('❌ WebSocket disconnected');
        });

    } catch (error) {
        console.warn('WebSocket not available:', error);
    }
}

// Update last updated timestamp
function updateLastUpdated() {
    const element = document.getElementById('lastUpdated');
    if (element) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
        element.textContent = `Updated at ${timeString}`;
    }
}

// Animate number values
function animateValue(element, start, end, duration, suffix = '') {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = current.toFixed(2) + suffix;
    }, 16);
}

// Refresh dashboard data
async function refreshDashboard() {
    console.log('🔄 Refreshing dashboard...');
    await loadAllMetrics();
    updateLastUpdated();
}

// Export functions for external use
window.dashboardAPI = {
    refresh: refreshDashboard,
    getCharts: () => charts
};
