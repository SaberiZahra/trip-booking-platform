window.renderChart = function (counts) {
    const ctx = document.getElementById('entityChart');
    if (!ctx) return;                       // اگر این صفحه نمودار ندارد

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['هتل‌ها', 'رستوران‌ها', 'کاربران', 'رزروها'],
            datasets: [{
                label: 'تعداد',
                data: [
                    counts.hotels,
                    counts.restaurants,
                    counts.users,
                    counts.reservations
                ]
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
};
  