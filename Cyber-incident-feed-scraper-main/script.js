document.addEventListener('DOMContentLoaded', function () {
    // Menu Item Active State Toggle and Content Switching
    let sideMenu = document.querySelectorAll(".nav-link");
    let sections = document.querySelectorAll(".content-section");

    // Variables for Charts (Initialized only when needed)
    let mySectorChart, myAptChart, myStrategicChart;

    // Handle section switching and content display
    if (sideMenu.length > 0) {
        sideMenu.forEach((item) => {
            let targetSection = document.getElementById(item.getAttribute("data-target"));

            item.addEventListener("click", () => {
                // Remove active state from all menu items
                sideMenu.forEach((link) => {
                    link.parentElement.classList.remove("active");
                });

                // Add active state to the clicked menu item
                item.parentElement.classList.add("active");

                // Hide all sections
                sections.forEach((section) => {
                    section.classList.add("hide");
                });

                // Show the target section
                if (targetSection) {
                    targetSection.classList.remove("hide");

                    // Load the feed if Feed Generator section is activated
                    if (targetSection.id === 'feed-gen') {
                        loadFeed();  // Load the feed when feed-gen section is shown
                    }

                    // Initialize and load charts for analytics when the Analytics section is activated
                    if (targetSection.id === 'dashboard') {
                        loadCyberInsights();  // Load the insights and charts
                    }
                } else {
                    console.error('Target section not found:', item.getAttribute("data-target"));
                }
            });
        });
    }

    // Function to load and display news from the JSON file
    function loadFeed() {
        const feedUrl = 'cyware_news.json';  // URL to your news feed JSON file
        const newsContainer = document.querySelector('#feed-gen .news-container');  // Target the container for the news feed
    
        fetch(feedUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                let html = '';
                if (data.length === 0) {
                    newsContainer.innerHTML = '<p>No news articles available.</p>';
                    return;
                }
                data.forEach(item => {
                    html += `
                    <div class="article">
                        <h2><a href="${item.link}" target="_blank">${item.title}</a></h2>
                        <p>${item.summary}</p>
                        <p><small>${item.date}</small></p>
                    </div>
                    `;
                });
                newsContainer.innerHTML = html;
            })
            .catch(error => {
                console.error('Error fetching or parsing the news feed:', error);
                newsContainer.innerHTML = '<p>Sorry, there was an error loading the news feed. Please try again later.</p>';
            });
    }

    // Function to load and display insights in the Analytics section
    function loadCyberInsights() {
        const insightsUrl = 'cyber_news_insights.json';  // URL to your insights JSON file
        const sectorChartElement = document.getElementById('sector-chart');
        const aptChartElement = document.getElementById('apt-chart');
        const strategicChartElement = document.getElementById('strategic-chart');
        const wciContainer = document.querySelector('.wci-container');
        fetch('cyber_crime_index.json')
            .then(response => response.json())
            .then(data => {
                const indiaWci = data.wci_score.India;
                wciContainer.innerHTML = `
                <h3>India's Cybersecurity Index</h3>
                <div class="wci-boxes">
                    <div class="wci-box">
                        <h4>WCI Score</h4>
                        <p>${indiaWci.score}</p>
                    </div>
                    <div class="wci-box">
                        <h4>World Rank</h4>
                        <p>#${indiaWci.rank}</p>
                    </div>
                </div>
            `;
            })
        
        fetch(insightsUrl)
            .then(response => response.json())
            .then(data => {
                // Destroy existing charts to avoid duplication
                if (mySectorChart) mySectorChart.destroy();
                if (myAptChart) myAptChart.destroy();
                if (myStrategicChart) myStrategicChart.destroy();
                
                // Visualize incidents by sector
                mySectorChart = new Chart(sectorChartElement.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: Object.keys(data.incidents_by_sector),
                        datasets: [{
                            label: 'Incidents by Sector',
                            data: Object.values(data.incidents_by_sector),
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });

                // Visualize APT involvement
                myAptChart = new Chart(aptChartElement.getContext('2d'), {
                    type: 'pie',
                    data: {
                        labels: Object.keys(data.apts_involved),
                        datasets: [{
                            label: 'APTs Involved',
                            data: Object.values(data.apts_involved),
                            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                        }]
                    }
                });

                // Visualize strategic issues
                myStrategicChart = new Chart(strategicChartElement.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: Object.keys(data.strategic_issues),
                        datasets: [{
                            label: 'Strategic Issues',
                            data: Object.values(data.strategic_issues),
                            backgroundColor: ['#4BC0C0', '#FF9F40', '#FF6384']
                        }]
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching insights:', error);
            });
    }

    // Dark Mode Toggle
    const switchMode = document.getElementById('switch-mode');

    // Check if dark mode was previously enabled
    if (localStorage.getItem('dark-mode') === 'enabled') {
        document.body.classList.add('dark');
        switchMode.checked = true;
    }

    // Toggle dark mode when switch is clicked
    switchMode.addEventListener('change', function () {
        if (this.checked) {
            document.body.classList.add('dark');
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            document.body.classList.remove('dark');
            localStorage.setItem('dark-mode', 'disabled');
        }
    });
    //service
    const modalViews=document.querySelectorAll('.services__modal'),
      modalBtns=document.querySelectorAll('.services__button'),
      modalClose=document.querySelectorAll('.services__modal-close')

let modal=function(modalClick){
    modalViews[modalClick].classList.add('active-modal')
}
modalBtns.forEach((mb,i)=>{
    mb.addEventListener('click',()=>{
        modal(i)
    })
})
modalClose.forEach((mc)=>{
    mc.addEventListener('click',()=>{
        modalViews.forEach((mv)=>{
            mv.classList.remove('active-modal')
        })
    })
})

    // Hamburger Menu Toggle
    const menuBtn = document.querySelector('.menu-btn');
    const sidebar = document.querySelector('.sidebar');

    // Toggle sidebar visibility on hamburger icon click
    menuBtn.addEventListener('click', function () {
        sidebar.classList.toggle('hide');  // Add or remove the 'hide' class
    });

});
