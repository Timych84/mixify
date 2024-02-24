
document.getElementById("createNewPlaylist").addEventListener("click", function() {
    var loadingSpinner = document.getElementById("loadingSpinner");
    var successMessage = document.getElementById("successMessage");
    var errorMessage = document.getElementById("errorMessage");
    var newPlaylistName = document.getElementById("newPlaylistName");
    var playlistName = newPlaylistName.value;
    var overwriteCheck = document.getElementById("overwriteCheck");
    var overwriteValue = overwriteCheck.checked;

    loadingSpinner.style.display = "block";
    successMessage.style.display = "none";
    errorMessage.style.display = "none";

    var data = {
        "playlist_name": playlistName,
        "overwrite": overwriteValue,
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/create_playlist", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            loadingSpinner.style.display = "none";
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    successMessage.style.display = "block";
                    successMessage.innerHTML = response.message; // Show success message
                    errorMessage.style.display = "none"; // Hide error message
                } else {
                    errorMessage.style.display = "block";
                    errorMessage.innerHTML = response.message; // Show error message
                    successMessage.style.display = "none"; // Hide success message
                }
            } else {
                errorMessage.style.display = "block";
                errorMessage.innerHTML = "HTTP error: " + xhr.status; // Show HTTP error message
                successMessage.style.display = "none"; // Hide success message
            }
        }
    };
    xhr.send(JSON.stringify(data));
});
