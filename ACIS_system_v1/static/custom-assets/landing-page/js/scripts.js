// Data for the charts
const chartData1 = {
    labels: ['Red', 'Blue', 'Yellow'],
    datasets: [{
        data: [30, 20, 50],
        backgroundColor: ['red', 'blue', 'yellow']
    }]
};

const chartData2 = {
    labels: ['A', 'B', 'C'],
    datasets: [{
        data: [25, 35, 40],
        backgroundColor: ['green', 'orange', 'purple']
    }]
};

const chartData3 = {
    labels: ['One', 'Two', 'Three'],
    datasets: [{
        data: [40, 30, 30],
        backgroundColor: ['pink', 'teal', 'lightblue']
    }]
};

const chartData4 = {
    labels: ['Apple', 'Orange', 'Banana'],
    datasets: [{
        data: [45, 20, 35],
        backgroundColor: ['orange', 'yellow', 'green']
    }]
};

// Chart configuration
const chartConfig = {
    type: 'doughnut',
    options: {
        responsive: true,
        aspectRatio: 1,
        cutoutPercentage: 70,
        // Add other options as needed
    }
};

// Create chart instances
const ctx1 = document.getElementById('chart1').getContext('2d');
const ctx2 = document.getElementById('chart2').getContext('2d');
const ctx3 = document.getElementById('chart3').getContext('2d');
const ctx4 = document.getElementById('chart4').getContext('2d');

// Create charts
const chart1 = new Chart(ctx1, {
    ...chartConfig,
    data: chartData1
});

const chart2 = new Chart(ctx2, {
    ...chartConfig,
    data: chartData2
});

const chart3 = new Chart(ctx3, {
    ...chartConfig,
    data: chartData3
});

const chart4 = new Chart(ctx4, {
    ...chartConfig,
    data: chartData4
});



//for arrow scroll up
// Show the button when user scrolls down 20px from the top of the document
window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("scrollToTopBtn").style.display = "block";
    } else {
        document.getElementById("scrollToTopBtn").style.display = "none";
    }
}

// Function to scroll to the top when the button is clicked
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
