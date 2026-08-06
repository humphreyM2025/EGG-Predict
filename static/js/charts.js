document.addEventListener('DOMContentLoaded', function() {
  fetch('/api/analytics-data')
    .then(response => response.json())
    .then(data => {
      // 1. Risk Distribution Chart
      new Chart(document.getElementById('riskDistChart'), {
        type: 'doughnut',
        data: {
          labels: Object.keys(data.risk_distribution),
          datasets: [{
            data: Object.values(data.risk_distribution),
            backgroundColor: ['#10b981', '#f59e0b', '#f97316', '#ef4444']
          }]
        }
      });

      // 2. Training Curves (Teacher vs Student Distillation metrics)
      new Chart(document.getElementById('accuracyCurveChart'), {
        type: 'line',
        data: {
          labels: data.training_metrics.epochs,
          datasets: [
            { label: 'Train Acc', data: data.training_metrics.train_acc, borderColor: '#0284c7', fill: false },
            { label: 'Val Acc', data: data.training_metrics.val_acc, borderColor: '#10b981', fill: false }
          ]
        }
      });
    });
});