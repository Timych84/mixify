document.addEventListener('DOMContentLoaded', function() {
    var animateBtn = document.getElementById('animateBtn');
    var bottomTile = document.getElementById('bottomTile');
    var newTileImages = document.getElementById('newTileImages');
    var playlistItems = document.querySelectorAll('.playlist-item');

    // Initial setup for the new tile (without images)
    newTileImages.style.width = '120px'; // Adjust the width based on your requirements
    newTileImages.style.height = '120px'; // Adjust the height based on your requirements
    newTileImages.style.background = '#f0f0f0'; // Adjust the background color if needed
    newTileImages.style.margin = 'auto'; // Center the new tile below the button
    newTileImages.style.opacity = '0'; // Set initial opacity to 0

    animateBtn.addEventListener('click', function() {
        // Get exactly 6 images from existing playlist items
        var selectedImages = getSelectedImages(playlistItems, 6);

        // Clear the existing content
        newTileImages.innerHTML = '';

        // Create new canvas element
        var canvas = document.createElement('canvas');
        canvas.width = 180; // Adjust the canvas size based on your requirements
        canvas.height = 120; // Adjust the canvas size based on your requirements

        // Get 2D context
        var context = canvas.getContext('2d');

        // Load each image and draw it on the canvas
        selectedImages.forEach(function(imageSrc, index) {
            var img = new Image();
            img.onload = function() {
                // Draw image on canvas
                context.drawImage(img, (index % 3) * 60, Math.floor(index / 3) * 60, 60, 60);

                // If all images are loaded, append canvas to the newTileImages div
                if (index === selectedImages.length - 1) {
                    // Set the new tile size with images
                    newTileImages.style.width = '180px'; // Adjust the width based on your requirements
                    newTileImages.style.height = '120px'; // Adjust the height based on your requirements

                    // Center the canvas within the div
                    canvas.style.margin = 'auto';
                    newTileImages.appendChild(canvas);

                    // Center the bottomTile under the button
                    bottomTile.style.margin = 'auto';

                    // Trigger the animation for each playlist item after the new tile is set up
                    animatePlaylistItems();
                }
            };
            img.src = imageSrc;
        });
    });

    // Function to get an array of exactly count images from existing playlist items
    function getSelectedImages(items, count) {
        var selectedImages = [];
        var imagesPool = [];

        // Collect all unique images from playlist items
        items.forEach(function(item) {
            var imgSrc = item.querySelector('img').src;
            if (!imagesPool.includes(imgSrc)) {
                imagesPool.push(imgSrc);
            }
        });

        // Shuffle the array to get a random order
        imagesPool.sort(() => Math.random() - 0.5);

        // Select exactly count images
        for (var i = 0; i < count; i++) {
            selectedImages.push(imagesPool[i]);
        }

        return selectedImages;
    }

    // Function to animate the playlist items
    function animatePlaylistItems() {
        // Calculate the position of the new tile
        var newTileRect = newTileImages.getBoundingClientRect();

        // Apply animation class to each playlist item for forward movement
        playlistItems.forEach(function(item) {
            var itemRect = item.getBoundingClientRect();

            // Calculate the translation values toward the new tile
            var translateX = newTileRect.left - itemRect.left;
            var translateY = newTileRect.top - itemRect.top;

            item.style.transition = 'transform 1s ease-in-out';
            item.style.transform = 'translate(' + translateX + 'px, ' + translateY + 'px)';
        });

        // After a delay, set opacity to 0 for all playlist items
        setTimeout(function() {
            playlistItems.forEach(function(item) {
                item.style.transition = 'opacity 0.5s ease-in-out';
                item.style.opacity = 0;
            });

            // Listen for the transitionend event on the last playlist item
            playlistItems[playlistItems.length - 1].addEventListener('transitionend', function() {
                // After the transition ends, set opacity to 1 for all playlist items
                playlistItems.forEach(function(item) {
                    item.style.transition = 'opacity 0.5s ease-in-out';
                    item.style.opacity = 1;
                });

                // Apply animation class to each playlist item for backward movement
                playlistItems.forEach(function(item) {
                    item.style.transition = 'transform 0.5s ease-in-out';
                    item.style.transform = 'translate(0, 0)';
                });

                // Make the new tile image visible with opacity transition
                setTimeout(function() {
                    newTileImages.style.opacity = '1';
                }, 100); // Adjust the delay (in milliseconds) based on your preference
            });
        }, 1000); // Adjust the delay (in milliseconds) based on your preference
    }

    // JavaScript code for the popup window
    var editIcon = document.getElementById('editIcon');
    var editPopup = document.getElementById('editPopup');
    var okButton = document.getElementById('okButton');
    var editableText = document.getElementById('editableText');
    var newTileText = document.getElementById('newTileText');

    editIcon.addEventListener('click', function() {
        showEditPopup();
    });

    okButton.addEventListener('click', function() {
        saveAndCloseEditPopup();
    });

    // Additional functions for the popup window
    function showEditPopup() {
        editPopup.style.display = 'block';
        document.getElementById('editPopupText').value = editableText.innerText;
    }

    function saveAndCloseEditPopup() {
        var editedText = document.getElementById('editPopupText').value;
        editableText.innerText = editedText;
        editPopup.style.display = 'none';
        // Update the text on the new tile
        newTileText.innerText = editedText;
    }
});
