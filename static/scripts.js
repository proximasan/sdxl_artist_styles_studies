document.getElementById('lightbox').classList.add('lightbox-hidden');

let currentImageIndex = 0;

function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}

// Modified navigateImages function
function navigateImages(direction, event) {
    if (event) {
        event.stopPropagation();
    }
    const galleryItems = document.querySelectorAll('.gallery-item');
    if (galleryItems.length > 0) {
        currentImageIndex = (currentImageIndex + direction + galleryItems.length) % galleryItems.length;
        const currentItem = galleryItems[currentImageIndex];
        const image1 = currentItem.querySelector('img:not(.hover-image)').src;
        const image2 = currentItem.querySelector('.hover-image').src;
        const artistName = currentItem.querySelector('h3').innerText;
        openLightbox(null, currentImageIndex, image1, image2, artistName);
    }
}

function handleKeyPress(event) {
    if (event.key === 'Escape') {
        closeLightbox();
    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
        navigateImages(-1);
    } else if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
        navigateImages(1);
    }
}

let scrollPosition;

function openLightbox(event, index, image1, image2, artistName) {
    if (event) {
        event.stopPropagation();
    }
    // Save the scroll position before opening the lightbox
    document.getElementById('lightbox').classList.remove('lightbox-hidden');
    scrollPosition = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
    document.body.style.top = `-${scrollPosition}px`;
    currentImageIndex = index;
    document.getElementById('lightboxImage1').src = image1;
    document.getElementById('lightboxImage2').src = image2;
    document.body.classList.add('lightbox-open');
    document.getElementById('lightboxCaption').innerText = artistName;
    document.querySelector('.artist-name-container').style.display = 'block';
    document.addEventListener('keydown', handleKeyPress);

    const artistUrl = `/artist/${encodeURIComponent(artistName)}`;
    history.pushState({ artistName }, artistName, artistUrl);

    document.getElementById('lightbox').addEventListener('touchstart', handleTouchStart, false);
    document.getElementById('lightbox').addEventListener('touchmove', handleTouchMove, false);
}

function closeLightbox(event) {
    if (!event || event.target === document.getElementById('lightbox') || event.target === document.getElementById('closeButton') || event.target === document.getElementById('closeIcon')) {
        document.getElementById('lightbox').classList.add('lightbox-hidden');
        window.scrollTo(0, scrollPosition);
        document.body.style.top = '';
        document.body.classList.remove('lightbox-open');
        document.querySelector('.artist-name-container').style.display = 'none';
        document.removeEventListener('keydown', handleKeyPress);
    }

    history.replaceState({}, document.title, '/');

    document.getElementById('lightbox').removeEventListener('touchstart', handleTouchStart, false);
    document.getElementById('lightbox').removeEventListener('touchmove', handleTouchMove, false);
}

function handleTouchStart(event) {
    this.startX = event.touches[0].clientX;
    this.startY = event.touches[0].clientY;
}

function handleTouchMove(event) {
    if (!this.startX || event.touches.length > 1) {
        return;
    }

    const xDiff = this.startX - event.touches[0].clientX;
    const yDiff = this.startY - event.touches[0].clientY;

    if (Math.abs(xDiff) > 50 && Math.abs(yDiff) < 100) {
        if (xDiff > 0) {
            navigateImages(1);
        } else {
            navigateImages(-1);
        }
        this.startX = null;
    }
}

function bindGalleryItemTouchEvents() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const maxTapTime = 300;  // Maximum time for a valid tap event (in ms)
    const maxTapDistance = 5;  // Maximum movement for a valid tap event (in pixels)

    galleryItems.forEach((item, index) => {
        let touchStartTime;
        let touchStartPos;
        let validTap = true;

        item.addEventListener('touchstart', (event) => {
            touchStartTime = Date.now();
            touchStartPos = { x: event.touches[0].clientX, y: event.touches[0].clientY };
        });

        item.addEventListener('touchmove', (event) => {
            const movePos = { x: event.touches[0].clientX, y: event.touches[0].clientY };
            const moveDistance = Math.sqrt(Math.pow(movePos.x - touchStartPos.x, 2) + Math.pow(movePos.y - touchStartPos.y, 2));

            if (moveDistance > maxTapDistance) {
                validTap = false;
            }
        });

        item.addEventListener('touchend', (event) => {
            if (!validTap) {
                validTap = true;
                return;
            }

            const touchEndTime = Date.now();
            const touchEndPos = { x: event.changedTouches[0].clientX, y: event.changedTouches[0].clientY };

            const tapDuration = touchEndTime - touchStartTime;
            const tapDistance = Math.sqrt(Math.pow(touchEndPos.x - touchStartPos.x, 2) + Math.pow(touchEndPos.y - touchStartPos.y, 2));

            if (tapDuration < maxTapTime && tapDistance < maxTapDistance) {
                const image1 = item.querySelector('img:not(.hover-image)').src;
                const image2 = item.querySelector('.hover-image').src;
                const artistName = item.querySelector('h3').innerText;
                openLightbox(event, index, image1, image2, artistName);
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Custom cursor code
    let customCursorActive = false; // Keep track of whether the custom cursor is active

    function toggleCustomCursor() {
        customCursorActive = !customCursorActive; // Toggle the state

        if (customCursorActive) {
            // Add the custom cursor class to the body
            document.body.classList.add('custom-cursor');
        } else {
            // Remove the custom cursor class from the body
            document.body.classList.remove('custom-cursor');
        }
    }

    document.getElementById('toggle-cursor-button').addEventListener('click', toggleCustomCursor);

    // Added double click event for button
    document.getElementById('toggle-cursor-button').addEventListener('dblclick', function (e) {
        // Define the array of image sources
        var images = ['static/1_48.png', 'static/2_48.png', 'static/3_48.png'];

        // Create 23 images
        for (let i = 0; i < 23; i++) {
            // Calculate a random index
            var randomIndex = Math.floor(Math.random() * images.length);

            // Create a new image element
            var img = document.createElement('img');
            img.src = images[randomIndex];
            img.className = 'raining-image'; // Assign the 'raining-image' class to the image

            // Randomly position the image on the page
            img.style.top = Math.random() * window.innerHeight + 'px';
            img.style.left = Math.random() * window.innerWidth + 'px';

            // Set random animation duration and no delay
            var duration = Math.random() * 3 + 2;  // Random duration between 2 and 5 seconds
            var delay = 0; // No delay
            img.style.animationDuration = duration + 's';
            img.style.animationDelay = delay + 's';

            // When animation ends, remove the image from the document
            img.addEventListener('animationend', function () {
                this.remove();
            });

            // Append the image to the body of the document
            document.body.appendChild(img);
        }
    });

    // Other code...
    bindGalleryItemTouchEvents();

    // Function to handle artist name copying
    function handleArtistNameCopy(artistNameElement) {
        artistNameElement.addEventListener("click", function (event) {
            // Only proceed if "data-is-copied" is not true
            if (this.getAttribute("data-is-copied") !== "true") {
                event.stopPropagation(); // Prevent triggering other click events

                // Create a new textarea element, set its value to the artist name, and add it to the document
                var textarea = document.createElement("textarea");
                textarea.value = this.innerText;
                document.body.appendChild(textarea);

                // Select the textarea's content and copy it to the clipboard
                textarea.select();
                document.execCommand("copy");

                // Remove the textarea from the document
                document.body.removeChild(textarea);

                // Change the text of the clicked element to "Copied ✓"
                var originalText = this.innerText;
                this.innerText = "copied ✓";

                // Set "data-is-copied" to true
                this.setAttribute("data-is-copied", "true");

                // Change the text back to the original after 3 seconds and set "data-is-copied" to false
                setTimeout(() => {
                    this.innerText = originalText;
                    this.setAttribute("data-is-copied", "false");
                }, 800);
            }
        });
    }

    // Get all elements with class="artist-name"
    var artistNames = document.getElementsByClassName("artist-name");

    // Loop through the elements, and add the copy to clipboard functionality
    for (var i = 0; i < artistNames.length; i++) {
        handleArtistNameCopy(artistNames[i]);
    }
});

function copyArtistNameToClipboard() {
    var artistNameElement = document.getElementById('artist-name');

    // Only proceed if "data-is-copied" is not true
    if (artistNameElement.getAttribute("data-is-copied") !== "true") {
        // Get the artist name
        var artistName = artistNameElement.innerText;

        // Create a new textarea element, set its value to the artist name, and add it to the document
        var textarea = document.createElement("textarea");
        textarea.value = artistName;
        document.body.appendChild(textarea);

        // Select the textarea's content and copy it to the clipboard
        textarea.select();
        document.execCommand("copy");

        // Remove the textarea from the document
        document.body.removeChild(textarea);

        // Change the text of the clicked element to "Copied ✓"
        var originalText = artistName;
        artistNameElement.innerText = "Copied ✓";

        // Set "data-is-copied" to true
        artistNameElement.setAttribute("data-is-copied", "true");

        // Change the text back to the original after 2 seconds and set "data-is-copied" to false
        setTimeout(() => {
            artistNameElement.innerText = originalText;
            artistNameElement.setAttribute("data-is-copied", "false");
        }, 800);
    }
}
