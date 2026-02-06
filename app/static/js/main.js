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

  const initialLimit = 10;
  const increment = 5;

  // Read the last saved limit from the hidden input, or default to 10
  let currentLimit = parseInt(isExpandedInput.value) || initialLimit;

  function updateVisibility() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const isSearching = searchTerm.length > 0;

    symptomItems.forEach((item, index) => {
      const label = item.querySelector('label');
      const text = label ? label.textContent.toLowerCase() : '';
      const matchesSearch = text.includes(searchTerm);
      const isChecked = item.querySelector('.symptom-checkbox').checked;

      if (isSearching) {
        // When searching, show all matching results
        item.style.display = matchesSearch ? 'block' : 'none';
      } else {
        // Show if: within current limit OR is checked (so user doesn't lose sight of picks)
        if (index < currentLimit || isChecked) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      }
    });

    // Manage "Show More" and "Show Less" button visibility
    if (isSearching) {
      showMoreBtn.style.display = 'none';
    } else {
      showMoreBtn.style.display = 'block';

      // If we reached the end of the list, change text to "Show Less"
      if (currentLimit >= symptomItems.length) {
        showMoreBtn.textContent = `Show Less (Reset to ${initialLimit})`;
      } else {
        const remaining = symptomItems.length - currentLimit;
        const nextStep = Math.min(increment, remaining);
        showMoreBtn.textContent = `Show More (+${nextStep})`;
      }
    }

    // Save current count to hidden input for Run Diagnosis persistence
    isExpandedInput.value = currentLimit;
  }

  searchInput.addEventListener('input', updateVisibility);

  showMoreBtn.addEventListener('click', function () {
    if (currentLimit >= symptomItems.length) {
      // Reset if user clicks while at the end
      currentLimit = initialLimit;
    } else {
      // Add 5 more
      currentLimit += increment;
    }
    updateVisibility();
  });

  clearBtn.addEventListener('click', function () {
    const checkboxes = document.querySelectorAll('.symptom-checkbox');
    checkboxes.forEach(cb => cb.checked = false);
    // Keep the current limit where it is
    updateVisibility();
  });

  updateVisibility();
});
