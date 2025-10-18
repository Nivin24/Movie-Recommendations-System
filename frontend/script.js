const recommendBtn = document.getElementById('recommendBtn');
const movieInput = document.getElementById('movieInput');
const resultsDiv = document.getElementById('results');
const loadingDiv = document.getElementById('loading');

movieInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault();
    recommendBtn.click();
  }
});

recommendBtn.addEventListener('click', async () => {
  const movieName = movieInput.value.trim();
  if (!movieName) {
    alert("Please enter a movie name!");
    return;
  }

  resultsDiv.innerHTML = "";
  loadingDiv.classList.remove('hidden');

  try {
    const response = await fetch('http://127.0.0.1:5000/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ movie: movieName })
    });

    const data = await response.json();
    loadingDiv.classList.add('hidden');

    if (data.recommended_movies && data.recommended_movies.length > 0) {
      for (const movie of data.recommended_movies) {
        const { posterUrl, backdropUrl, overview } = await fetchMovieDetails(movie);

        const card = document.createElement('div');
        card.className = "group perspective";

        card.innerHTML = `
          <div class="relative w-full h-96 transition-transform duration-700 transform-style-preserve-3d group-hover:rotate-y-180">
            <!-- Front -->
            <div class="absolute w-full h-full backface-hidden rounded-lg overflow-hidden shadow-md">
              <img src="${backdropUrl}" alt="${movie}" class="absolute inset-0 w-full h-full object-cover opacity-50">
              <img src="${posterUrl}" alt="${movie}" class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 w-40 h-56 object-cover rounded-lg shadow-lg">
              <div class="absolute bottom-0 w-full bg-gray-800 bg-opacity-70 p-2 text-white text-center text-lg font-semibold">${movie}</div>
            </div>

            <!-- Back -->
            <div class="absolute w-full h-full backface-hidden rotate-y-180 bg-white rounded-lg p-4 flex flex-col justify-start overflow-auto">
              <h3 class="text-lg font-semibold text-gray-900 mb-2">${movie}</h3>
              <p class="text-sm overflow-y-auto max-h-full">${overview}</p>
            </div>
          </div>
        `;

        resultsDiv.appendChild(card);
      }
    } else {
      resultsDiv.innerHTML = "<p class='text-red-500 text-center col-span-full'>No recommendations found.</p>";
    }
  } catch (error) {
    console.error(error);
    loadingDiv.classList.add('hidden');
    resultsDiv.innerHTML = "<p class='text-red-500 text-center col-span-full'>Error fetching recommendations.</p>";
  }
});

// Fetch movie images
async function fetchMovieDetails(movieTitle) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/poster/${encodeURIComponent(movieTitle)}`);
    const data = await response.json();

    return {
      posterUrl: data.poster_url || "https://via.placeholder.com/500x750?text=No+Poster",
      backdropUrl: data.poster_url || "https://via.placeholder.com/780x439?text=No+Backdrop",
      overview: data.overview || "No description available."
    };
  } catch (error) {
    console.error(`Error fetching details for "${movieTitle}":`, error);
    return {
      posterUrl: "https://via.placeholder.com/500x750?text=No+Poster",
      backdropUrl: "https://via.placeholder.com/780x439?text=No+Backdrop",
      overview: "No description available."
    };
  }
}