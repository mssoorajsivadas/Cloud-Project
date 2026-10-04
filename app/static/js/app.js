/* 
#===========================#

        Signup Page       

#===========================#
*/
const registerForm = document.getElementById("signup-form");
if (registerForm) {

    registerForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const firstName = document.getElementById("first-name").value;
        const secondName = document.getElementById("second-name").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;

        if (password.value !== confirmPassword.value) {

            showMessage(
                "Passwords do not match",
                "error"
            );

            return;
        }

        const response = await fetch("/api/auth/register", {

            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                first_name: firstName,
                second_name: secondName,
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {

            showMessage(
                data.message,
                "success"
            )

            registerForm.reset();

            setTimeout(() => {
                window.location.href = "/signin";
            }, 1000);

        } else {

            showMessage(
                data.message,
                "error"
            )
        }
    });
}

/* 
#===========================#

        Signin Page       

#===========================#
*/
const loginForm = document.getElementById("signin-form");

if (loginForm) {

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const login = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const response = await fetch("/api/auth/login", {

            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify({
                login: login,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {

            showMessage(
                data.message,
                "success"
            )

            loginForm.reset();

            window.location.href = "/drive";


        } else {

            showMessage(
                data.message,
                "error"
            )
        }
    });
}

/* 
#===========================#

        Logout Page       

#===========================#
*/
const logoutButton = document.getElementById("logout-button");

if (logoutButton) {

    logoutButton.addEventListener("click", async function () {

        const response = await fetch("/api/auth/logout", {

            method: "POST"

        });

        const data = await response.json();

        if (response.ok) {

            window.location.href = "/signin";

        }

    });

}