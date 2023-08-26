document.addEventListener('DOMContentLoaded', () => {
    const loadingAnimation = document.getElementById('loading-animation');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const originalTitle = document.title;
    const searchContainer = document.getElementById('search-container');
    const errorTextContainer = document.getElementById('error-text-container')
    const buttonContainer = document.getElementById('button-container');
    const embedContainer = document.querySelector('.embed-container');
    const resultContainer = document.getElementById('result-container');
    const body = document.body;
    const html = document.documentElement;

    // Create a background element for the image
    const backgroundElement = document.createElement('div');
    backgroundElement.classList.add('background-image');
    html.appendChild(backgroundElement); // Adding to `html` not `body` !!

    // Hide the loading animation
    loadingAnimation.style.display = 'none';


    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();  // Prevent the default form submission behavior (refresh the page)

        // Animate the search bar to move it to the header
        searchContainer.style.animation = 'moveToHeader 0.5s forwards';
        searchInput.style.animation = 'widthAnimationHeader 0.5s forwards';

        // Show the loading animation
        loadingAnimation.style.display = 'block';

        const searchInputValue = searchInput.value;

        // Send a POST request to the '/search' route (Flask: app.py)
        const response = await fetch('/search', {
            method: 'POST',
            body: new URLSearchParams({ yt_url: searchInputValue }),
        });

        // Parse the response as JSON
        const data = await response.json();

        // Clear the previous content
        errorTextContainer.textContent = '';
        buttonContainer.textContent = '';
        embedContainer.textContent = '';

        // Check if the response contains an error message
        if (data.result.error) {
            loadingAnimation.style.display = 'none'; // Hide the loading animation
            errorTextContainer.textContent = data.result.error; // Display the error message
        } else {

            // Update the title of the page to 'Music by Artists'
            document.title = `Yutify | ${data.result.title} by ${data.result.artists}`;

            // Insert the Spotify embed into the embed container
            embedContainer.innerHTML = data.result.embed;
            
            // Create a button element as a link
            const linkButton = document.createElement('button');
            linkButton.className = 'buttons';
            linkButton.textContent = 'Open in Spotify';
            linkButton.addEventListener('click', () => {
                window.open(data.result.url, '_blank');  // Open the link in a new tab
            });
        
            // Add the link button to the result container
            buttonContainer.appendChild(linkButton);

            loadingAnimation.style.display = 'none'; // Hide the loading animation

            // Apply the background image and blur effect to the background element
            body.style.background = 'none'; // Remove body background color
            backgroundElement.style.backgroundImage = `url(${data.result.album_art})`;
            backgroundElement.style.filter = 'blur(3px)';
        }
    });

    // Check for input field focus
    searchInput.addEventListener('focus', () => {
        const containerStyle = window.getComputedStyle(searchContainer);
        
        // Check if the transform value matches
        // to make sure the search bar is on top
        if (containerStyle.animationName === 'moveToHeader') {

            // Reset the title to the original value
            document.title = originalTitle;
            
            // Apply animation to elements
            searchContainer.style.animation = 'moveToBody 0.5s forwards';
            searchInput.style.animation = 'widthAnimationBody 0.5s forwards';
            buttonContainer.style.animation = 'fadeOut 0.5s forwards';
            resultContainer.style.zIndex = '-1';
            embedContainer.style.animation = 'scaleDown 0.5s forwards';
            backgroundElement.style.animation = 'fadeOut 1s forwards';
            resultContainer.style.animation = 'fadeOut 0.5s forwards';
            
            // Clear previous content after the animation completes
            setTimeout(() => {
                // Clear the text field
                searchInput.value = '';
                errorTextContainer.textContent = '';
                buttonContainer.textContent = '';
                embedContainer.textContent = '';

                backgroundElement.style.backgroundImage = 'none'; // Remove the background image

                // Remove animations from elements
                searchContainer.style.animation = 'none';
                searchInput.style.animation = 'none';
                buttonContainer.style.animation = 'none';
                embedContainer.style.animation = 'none';
                backgroundElement.style.animation = 'none';
                resultContainer.style.animation = 'none';

                // Reset z-index after animation
                resultContainer.style.zIndex = '';
            }, 500); // Wait for 0.5s (to make sure the animation completes)
        }
    });
});
