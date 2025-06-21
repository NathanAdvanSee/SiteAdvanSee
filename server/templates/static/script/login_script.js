// static/js/login_script.js

function togglePasswordVisibility() {
    var passwordField = document.getElementById("password");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

function validateLoginForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    if (username === "" || password === "") {
        alert("Please fill in both fields.");
        return false;
    }

    // Additional validation can be added here

    return true; // Form is valid
}
function submitLoginForm(event) {
    event.preventDefault(); // Prevent the default form submission

    if (validateLoginForm()) {
        // If the form is valid, submit it
        document.getElementById("loginForm").submit();
    }
}