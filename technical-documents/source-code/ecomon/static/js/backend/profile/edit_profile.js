
function popupEditUsername() {
    _showPopup();
    var popupContent = document.getElementById('popup-content');
}

function closePopup() {
    var popupContainer = document.getElementById('popup-container');
    popupContainer.classList.add("hidden");
}

function _showPopup(){
    var popupContainer = document.getElementById('popup-container');
    popupContainer.classList.remove("hidden");
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("edit-username-form");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent regular form submit

        const usernameInput = document.getElementById("new-username");
        const feedbackDiv = document.getElementById("username-feedback");

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/accounts/api/profile/update/username/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                new_username: usernameInput.value
            })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200) {
                feedbackDiv.textContent = body.message;
                feedbackDiv.style.color = "green";
                // Optionally reload the page or update username display in real-time
                setTimeout(() => window.location.reload(), 1000);
            } else {
                feedbackDiv.textContent = Object.values(body).flat().join(", ");
                feedbackDiv.style.color = "red";
            }
        })
        .catch(error => {
            feedbackDiv.textContent = "Something went wrong.";
            feedbackDiv.style.color = "red";
            console.error("Error:", error);
        });
    });
});
