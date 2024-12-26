async function fetchChampionStats(champion = '') {
    try {
        const response = await fetch(`http://localhost:3000/champion-stats?champion=${champion}`);
        const result = await response.json();
        const { data } = result;
        const statsDiv = document.getElementById('champion-stats');

        // Clear existing content
        statsDiv.innerHTML = '';

        if (!data) {
            statsDiv.textContent = 'No data found for the specified champion.';
            return;
        }

        // Display champion stats
        const statDiv = document.createElement('div');
        statDiv.className = 'p-4 border-b';
        statDiv.innerHTML = `
            <p><strong>Champion Name:</strong> ${data.championName}</p>
            <p><strong>Win Percent:</strong> ${data.winPercent}%</p>
            <p><strong>Total Games:</strong> ${data.totalGames}</p>
        `;
        statsDiv.appendChild(statDiv);
    } catch (error) {
        console.error('Error fetching champion stats:', error);
    }
}

// Handle search form submission
document.getElementById('search-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const champion = document.getElementById('champion-input').value;
    fetchChampionStats(champion);
});