// Functions to open the corresponding popup
function popupEditUsername() {
    _showGeneralPopup();
    document.getElementById('popup-edituser').classList.remove("hidden");
}

function popupEditEmail() {
    _showGeneralPopup();
    document.getElementById('popup-editemail').classList.remove("hidden");
}

function popupEditPassword() {
    _showGeneralPopup();
    document.getElementById('popup-container-password').classList.remove("hidden");
}

function _showGeneralPopup(){
    document.getElementById('popup-container').classList.remove("hidden");
}

// Generic close function: closes the popup that contains the clicked element
function closePopup(element) {
    document.getElementById('popup-container').classList.add("hidden");
    document.getElementById('popup-edituser').classList.add("hidden");
    document.getElementById('popup-editemail').classList.add("hidden");
    document.getElementById('popup-container-password').classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", function () {
    // Update Username
    const usernameForm = document.getElementById("edit-username-form");
    usernameForm.addEventListener("submit", function (e) {
        e.preventDefault();
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

    // Update Email
    const emailForm = document.getElementById("edit-email-form");
    emailForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const emailInput = document.getElementById("new-email");
        const feedbackDiv = document.getElementById("email-feedback");
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/accounts/api/profile/update/email/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                new_email: emailInput.value
            })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200) {
                feedbackDiv.textContent = body.message;
                feedbackDiv.style.color = "green";
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

    // Update Password
    const passwordForm = document.getElementById("edit-password-form");
    passwordForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const oldPasswordInput = document.getElementById("old-password");
        const newPasswordInput = document.getElementById("new-password");
        const confirmNewPasswordInput = document.getElementById("confirm-new-password");
        const feedbackDiv = document.getElementById("password-feedback");
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/accounts/api/profile/update/password/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                old_password: oldPasswordInput.value,
                new_password: newPasswordInput.value,
                confirm_new_password: confirmNewPasswordInput.value
            })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200) {
                feedbackDiv.textContent = body.message;
                feedbackDiv.style.color = "green";
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
