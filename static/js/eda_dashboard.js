(function () {
    const data = window.dashboardData;
    if (!data || typeof Chart === "undefined") {
        return;
    }

    const fontFamily = "'Inter', sans-serif";

    Chart.defaults.color = "#345069";
    Chart.defaults.font.family = fontFamily;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;

    const liveStatus = document.getElementById("liveStatus");
    const lastUpdatedEl = document.getElementById("lastUpdated");
    let lastRefreshAt = Date.now();

    const setLastUpdatedText = () => {
        if (!lastUpdatedEl) {
            return;
        }
        const ts = new Date(lastRefreshAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        lastUpdatedEl.textContent = `Last updated: ${ts}`;
    };

    const hasPoints = (series) => {
        return Array.isArray(series) && series.length > 0;
    };

    const makeChart = (canvasId, config) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            return;
        }
        // Skip rendering for empty datasets to avoid noisy empty charts.
        if (config._empty) {
            const noData = document.createElement("p");
            noData.textContent = "No data available for this chart in the current dataset.";
            noData.style.color = "#6b839c";
            noData.style.fontStyle = "italic";
            canvas.replaceWith(noData);
            return;
        }
        new Chart(canvas, config);
    };

    const income = data.income_coverage || {};
    makeChart("incomeCoverageChart", {
        type: "bar",
        _empty: !hasPoints(income.labels),
        data: {
            labels: income.labels || [],
            datasets: [
                {
                    label: "Coverage Rate (%)",
                    data: income.coverage || [],
                    backgroundColor: "rgba(11, 94, 215, 0.72)",
                    borderColor: "#0b5ed7",
                    borderWidth: 1,
                    yAxisID: "y"
                },
                {
                    label: "Sample Size",
                    data: income.counts || [],
                    type: "line",
                    borderColor: "#ed7d31",
                    backgroundColor: "rgba(237, 125, 49, 0.2)",
                    pointRadius: 3,
                    yAxisID: "y1",
                    tension: 0.2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            scales: {
                y: { beginAtZero: true, suggestedMax: 100, title: { display: true, text: "Coverage %" } },
                y1: {
                    beginAtZero: true,
                    position: "right",
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: "Records" }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (ctx) {
                            if (ctx.dataset.label === "Coverage Rate (%)") {
                                return `Coverage: ${ctx.parsed.y}%`;
                            }
                            return `Records: ${ctx.parsed.y}`;
                        }
                    }
                }
            }
        }
    });

    const checkups = data.checkup_frequency || {};
    makeChart("checkupFrequencyChart", {
        type: "doughnut",
        _empty: !hasPoints(checkups.labels),
        data: {
            labels: checkups.labels || [],
            datasets: [
                {
                    label: "People",
                    data: checkups.counts || [],
                    backgroundColor: ["#198754", "#dc3545"],
                    borderWidth: 2,
                    borderColor: "#ffffff"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        afterLabel: function (ctx) {
                            const coverage = (checkups.coverage || [])[ctx.dataIndex];
                            return `Coverage rate: ${coverage || 0}%`;
                        }
                    }
                }
            }
        }
    });

    const conditions = data.common_conditions || {};
    makeChart("conditionsChart", {
        type: "bar",
        _empty: !hasPoints(conditions.labels),
        data: {
            labels: conditions.labels || [],
            datasets: [
                {
                    label: "Prevalence (%)",
                    data: conditions.prevalence || [],
                    backgroundColor: "rgba(220, 53, 69, 0.72)",
                    borderColor: "#dc3545",
                    borderWidth: 1
                },
                {
                    label: "Insured within condition group (%)",
                    data: conditions.coverage || [],
                    type: "line",
                    borderColor: "#0d6efd",
                    pointRadius: 3,
                    tension: 0.25
                }
            ]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { beginAtZero: true, suggestedMax: 100 }
            }
        }
    });

    const visits = data.hospital_visit_pattern || {};
    makeChart("visitPatternChart", {
        type: "line",
        _empty: !hasPoints(visits.labels),
        data: {
            labels: visits.labels || [],
            datasets: [
                {
                    label: "Coverage Rate (%)",
                    data: visits.coverage || [],
                    borderColor: "#20c997",
                    backgroundColor: "rgba(32, 201, 151, 0.18)",
                    fill: true,
                    tension: 0.32,
                    pointRadius: 3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, suggestedMax: 100 }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        afterLabel: function (ctx) {
                            const count = (visits.counts || [])[ctx.dataIndex];
                            return `Records: ${count || 0}`;
                        }
                    }
                }
            }
        }
    });

    const employment = data.employment_coverage || {};
    makeChart("employmentCoverageChart", {
        type: "bar",
        _empty: !hasPoints(employment.labels),
        data: {
            labels: employment.labels || [],
            datasets: [
                {
                    label: "Coverage Rate (%)",
                    data: employment.coverage || [],
                    backgroundColor: "rgba(255, 193, 7, 0.72)",
                    borderColor: "#ffc107",
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, suggestedMax: 100 } },
            plugins: {
                tooltip: {
                    callbacks: {
                        afterLabel: function (ctx) {
                            const count = (employment.counts || [])[ctx.dataIndex];
                            return `Records: ${count || 0}`;
                        }
                    }
                }
            }
        }
    });

    setLastUpdatedText();

    const refreshOnFocus = () => {
        const now = Date.now();
        const minutesSince = (now - lastRefreshAt) / 60000;
        if (minutesSince >= 1) {
            if (liveStatus) {
                liveStatus.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Refreshing...';
            }
            window.location.reload();
        }
    };

    window.addEventListener("focus", refreshOnFocus);
    document.addEventListener("visibilitychange", function () {
        if (document.visibilityState === "visible") {
            refreshOnFocus();
        }
    });

    // Hard refresh the dashboard data every 2 minutes while page is open.
    window.setInterval(function () {
        if (liveStatus) {
            liveStatus.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Updating...';
        }
        window.location.reload();
    }, 120000);
})();
