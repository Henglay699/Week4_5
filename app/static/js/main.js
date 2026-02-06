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

// Wait until the page loads
document.addEventListener("DOMContentLoaded", function () {
  // Select all alerts
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    // Set timeout to remove after 2 seconds (2000 ms)
    setTimeout(function () {
      // Use Bootstrap's built-in fade out
      alert.classList.remove('show'); // hides with fade
      alert.classList.add('fade');    // ensures transition
      // setTimeout(() => alert.remove());
    }, 4000);
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('symptomSearch');
  const symptomItems = document.querySelectorAll('.symptom-item');
  const clearBtn = document.getElementById('clearAll');
  const showMoreBtn = document.getElementById('showMoreBtn');
  const isExpandedInput = document.getElementById('isExpandedInput');

  const limit = 3;
  // Initialize state from the hidden input (survives page reload)
  let isExpanded = isExpandedInput.value === 'true';

  function updateVisibility() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const isSearching = searchTerm.length > 0;

    symptomItems.forEach((item, index) => {
      const label = item.querySelector('label');
      const text = label ? label.textContent.toLowerCase() : '';
      const matchesSearch = text.includes(searchTerm);
      const isChecked = item.querySelector('.symptom-checkbox').checked;

      if (isSearching) {
        item.style.display = matchesSearch ? 'block' : 'none';
      } else {
        // Stay visible if: Expanded OR it's in the first 3 OR it's currently checked
        if (isExpanded || index < limit || isChecked) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      }
    });

    if (isSearching || symptomItems.length <= limit) {
      showMoreBtn.style.display = 'none';
    } else {
      showMoreBtn.style.display = 'block';
      showMoreBtn.textContent = isExpanded ? 'Show Less' : `Show More Symptoms (+${symptomItems.length - limit})`;
    }

    // Update hidden input so the server knows state on next submit
    isExpandedInput.value = isExpanded;
  }

  searchInput.addEventListener('input', updateVisibility);

  showMoreBtn.addEventListener('click', function () {
    isExpanded = !isExpanded;
    updateVisibility();
  });

  clearBtn.addEventListener('click', function () {
    // Just uncheck everything
    const checkboxes = document.querySelectorAll('.symptom-checkbox');
    checkboxes.forEach(cb => cb.checked = false);

    // DO NOT reset isExpanded here. 
    // We leave it exactly as the user had it.
    updateVisibility();
  });

  // Run on page load
  updateVisibility();
});
