const toggleLink = document.getElementById("toggle-form");
const formTitle = document.getElementById("form-title");
const emailField = document.getElementById("email-field");

let isLogin = true;

toggleLink.addEventListener("click", (e) => {
    e.preventDefault();
    isLogin = !isLogin;

    if (isLogin) {
        formTitle.textContent = "ورود به حساب کاربری";
        toggleLink.textContent = "ثبت‌نام کنید";
        emailField.classList.add("hidden");
    } else {
        formTitle.textContent = "ثبت‌نام کاربر جدید";
        toggleLink.textContent = "ورود به حساب";
        emailField.classList.remove("hidden");
    }
});
