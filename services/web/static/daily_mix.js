document.getElementById("showNewPlaylist").addEventListener("click", function() {
    var mergedImagesContainer = document.getElementById("mergedImagesContainer");
    var loadingSpinner = document.getElementById("loadingSpinner");
    var successMessage = document.getElementById("successMessage");
    var errorMessage = document.getElementById("errorMessage");
    var cardTitleInput = document.getElementById("cardTitleInput");
    var playlistName = cardTitleInput.value;
    var overwriteCheck = document.getElementById("overwriteCheck");
    var overwriteValue = overwriteCheck.checked;
    var cardTitle = document.getElementById("cardTitle");

    mergedImagesContainer.style.display = "none";
    loadingSpinner.style.display = "block";
    successMessage.style.display = "none";
    errorMessage.style.display = "none";
    cardTitle.textContent = playlistName;

    var mergedImagesDiv = document.getElementById("mergedImages");
    mergedImagesDiv.innerHTML = "";

    var playlistImageURLs = playlists_info.map(function(playlist) {
        return playlist.images;
    });

    playlistImageURLs = shuffle(playlistImageURLs);

    var playlistIDs = playlists_info.map(function(playlist) {
        return playlist.id;
    });

    playlistImageURLs.forEach(function(url) {
        var img = document.createElement("img");
        img.src = url;
        img.style.width = "33.33%";
        img.style.height = "auto";
        mergedImagesDiv.appendChild(img);
    });

    var data = {
        "playlist_name": playlistName,
        "overwrite": overwriteValue,
        "playlists": playlistIDs
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/create_daily_mix", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            loadingSpinner.style.display = "none";
            if (xhr.status === 200) {
                successMessage.style.display = "block";
                mergedImagesContainer.style.display = "flex";
            } else {
                errorMessage.style.display = "block";
                mergedImagesContainer.style.display = "flex";
            }
        }
    };
    xhr.send(JSON.stringify(data));
});

// document.getElementById("updateTitleButton").addEventListener("click", function() {
//     var cardTitleInput = document.getElementById("cardTitleInput");
//     var cardTitle = document.getElementById("cardTitle");
//     cardTitle.textContent = cardTitleInput.value;
// });

function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
    while (0 !== currentIndex) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }
    return array;
}
