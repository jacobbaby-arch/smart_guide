document.getElementById("searchForm").addEventListener("submit", function (event) {
    event.preventDefault();
    
    // Get user input
    const destination = document.getElementById("destination").value;

    // Clear previous results
    const resultsContainer = document.getElementById("destinationResults");
    resultsContainer.innerHTML = "";

    // Simulate AI-generated recommendations (You will replace this with your AI logic)
    const recommendations = [
        {
            name: "Paris, France",
            image: "https://via.placeholder.com/300x200?text=Paris",
            description: "Known for its art, fashion, and culture.",
        },
        {
            name: "Tokyo, Japan",
            image: "https://via.placeholder.com/300x200?text=Tokyo",
            description: "Famous for its technology and cherry blossoms.",
        },
        {
            name: "New York, USA",
            image: "https://via.placeholder.com/300x200?text=New+York",
            description: "The city that never sleeps. A cultural hub.",
        },
    ];

    // Display the recommendations
    recommendations.forEach(function (destination) {
        const card = document.createElement("div");
        card.classList.add("destination-card");

        card.innerHTML = `
            <img src="${destination.image}" alt="${destination.name}">
            <h3>${destination.name}</h3>
            <p>${destination.description}</p>
        `;
        resultsContainer.appendChild(card);
    });
});
