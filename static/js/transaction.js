document.addEventListener("DOMContentLoaded", function () {
    console.log("Page loaded, fetching data...");

    fetch("http://127.0.0.1:5000/transactions/data")
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data:", data);

            if (!data.expenses || !data.earnings) {
                console.error("Invalid data format:", data);
                return;
            }
           
           

            const expenseCategories = data.expenses.map(item => item.category);
            const expenseAmounts = data.expenses.map(item => item.amount);
            const earningCategories = data.earnings.map(item => item.category);
            const earningAmounts = data.earnings.map(item => item.amount);

            if (!document.getElementById("expenseChart") || !document.getElementById("earningChart")) {
                console.error("Canvas elements missing!");
                return;
            }

            let expenseChart, earningChart;

            // Function to reset canvas size before creating a new chart
            function resetCanvas(chartId) {
                let canvas = document.getElementById(chartId);
                let parent = canvas.parentNode;

                parent.removeChild(canvas); // Remove existing canvas
                let newCanvas = document.createElement("canvas");
                newCanvas.id = chartId;
                newCanvas.width = 400; // Set fixed width
                newCanvas.height = 200; // Set fixed height
                parent.appendChild(newCanvas);
                return newCanvas.getContext("2d");
            }

            // Expenses Chart
            function create_expense_chart(type) {
                if (expenseChart) expenseChart.destroy();
                const expenseCtx = resetCanvas("expenseChart"); // Reset canvas size

                expenseChart = new Chart(expenseCtx, {
                    type: type,
                    data: {
                        labels: expenseCategories,
                        datasets: [{
                            label: "Expenses",
                            data: expenseAmounts,
                            backgroundColor: "rgba(255, 99, 132, 0.6)",
                            borderColor: "rgba(255, 99, 132, 1)",
                            borderWidth: 1
                        }]
                    },
                    options: { 
                        responsive: true, 
                        maintainAspectRatio: false // Prevent auto-resizing
                    }
                });
            }
            create_expense_chart("pie");

            document.getElementById('ExpenseChartOpt').addEventListener("change", function () {
                create_expense_chart(this.value);
            });

            // Earnings Chart
            function create_earning_chart(type) {
                if (earningChart) earningChart.destroy();
                const earningCtx = resetCanvas("earningChart"); // Reset canvas size

                earningChart = new Chart(earningCtx, {
                    type: type,
                    data: {
                        labels: earningCategories,
                        datasets: [{
                            label: "Earnings",
                            data: earningAmounts,
                            backgroundColor: "rgba(54, 162, 235, 0.6)",
                            borderColor: "rgba(54, 162, 235, 1)",
                            borderWidth: 1
                        }]
                    },
                    options: { 
                        responsive: true, 
                        maintainAspectRatio: false 
                    }
                });
            }
            create_earning_chart("pie");

            document.getElementById('EarningChartOpt').addEventListener("change", function () {
                create_earning_chart(this.value);
            });

            console.log("Charts rendered successfully!");
        })
        .catch(error => console.error("Error fetching data:", error));
});

