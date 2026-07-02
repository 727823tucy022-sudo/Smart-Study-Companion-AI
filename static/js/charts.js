// Verification Wrapper isolating Chart configurations from throwing runtime errors on non-dashboard templates
function initializeClientSideCharts(metaMetrics) {
    if (!document.getElementById('modelComparisonChart')) return;

    const labels = Object.keys(metaMetrics);
    const accuracyData = labels.map(key => metaMetrics[key].accuracy * 100);
    const f1Data = labels.map(key => metaMetrics[key].f1_score * 100);

    // Multi-algorithm Comparison Bar Chart
    const ctxBar = document.getElementById('modelComparisonChart').getContext('2d');
    new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Accuracy (%)',
                    data: accuracyData,
                    backgroundColor: 'rgba(99, 102, 241, 0.75)',
                    borderColor: '#6366f1',
                    borderWidth: 1.5
                },
                {
                    label: 'F1 Score (%)',
                    data: f1Data,
                    backgroundColor: 'rgba(236, 72, 153, 0.75)',
                    borderColor: '#ec4899',
                    borderWidth: 1.5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: document.body.classList.contains('dark-theme') ? '#fff' : '#000' } }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: document.body.classList.contains('dark-theme') ? '#ccc' : '#333' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: document.body.classList.contains('dark-theme') ? '#ccc' : '#333' }
                }
            }
        }
    });
}