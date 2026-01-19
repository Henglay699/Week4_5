document.addEventListener("DOMContentLoaded", () => {
  const pwd = document.querySelector('input[name="password"]');
  if (!pwd) return;

  pwd.addEventListener("input", () => {
    const msg = document.querySelector("#passwordHelp");
    if (!msg) return;

    const v = pwd.value;
    const strong =
      v.length >= 8 &&
      /[A-Z]/.test(v) &&
      /[a-z]/.test(v) &&
      /[0-9]/.test(v) &&
      /[!@#$%^&*(),.?":{}|<>_\-+=]/.test(v);

    msg.textContent = strong
      ? "Strong password ✅"
      : "Use at least 8 chars, with upper, lower, number, and special symbol.";
    msg.className = strong ? "form-text text-success" : "form-text text-danger";
  });
});

// // Wait until the page loads
// document.addEventListener("DOMContentLoaded", function() {
//   // Select all alerts
//   const alerts = document.querySelectorAll('.alert');
//   alerts.forEach(function(alert) {
//     // Set timeout to remove after 2 seconds (2000 ms)
//     setTimeout(function () {
//       // Use Bootstrap's built-in fade out
//       alert.classList.remove('show'); // hides with fade
//       alert.classList.add('fade');    // ensures transition
//       // setTimeout(() => alert.remove());
//     }, 4000);
//   });
// });


