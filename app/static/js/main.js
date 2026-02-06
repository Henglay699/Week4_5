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

  // 1. Existing Search Logic
  searchInput.addEventListener('input', function () {
    const searchTerm = searchInput.value.toLowerCase();
    symptomItems.forEach(item => {
      const text = item.querySelector('label').textContent.toLowerCase();
      item.style.display = text.includes(searchTerm) ? 'block' : 'none';
    });
  });

  // 2. Clear All Logic
  clearBtn.addEventListener('click', function () {
    const checkboxes = document.querySelectorAll('.symptom-checkbox');
    checkboxes.forEach(cb => cb.checked = false);

    // Optional: Reset search view too
    searchInput.value = '';
    symptomItems.forEach(item => item.style.display = 'block');
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const symptomItems = document.querySelectorAll('.symptom-item');
  const showMoreBtn = document.getElementById('showMoreBtn');
  const limit = 4;
  let isExpanded = false;

  // 1. Initial State: If more than 30, hide the rest
  if (symptomItems.length > limit) {
    showMoreBtn.style.display = 'block';
    updateVisibility();
  }

  function updateVisibility() {
    symptomItems.forEach((item, index) => {
      // If expanded, show all. If not, only show up to the limit.
      if (isExpanded) {
        item.style.display = 'block';
      } else {
        item.style.display = index < limit ? 'block' : 'none';
      }
    });
  }

  // 2. Click Event for Show More / Show Less
  showMoreBtn.addEventListener('click', function () {
    isExpanded = !isExpanded;
    updateVisibility();
    this.textContent = isExpanded ? 'Show Less' : 'Show More Symptoms';

    // If they hide items, scroll back to the top of the list
    if (!isExpanded) {
      document.getElementById('fact-list').scrollTop = 0;
    }
  });

  // 3. INTEGRATION WITH SEARCH: 
  // We must disable "Show More" logic while the user is searching
  const searchInput = document.getElementById('symptomSearch');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const hasValue = this.value.trim().length > 0;
      if (hasValue) {
        showMoreBtn.style.display = 'none'; // Hide button during search
      } else if (symptomItems.length > limit) {
        showMoreBtn.style.display = 'block'; // Bring back button if search cleared
        updateVisibility();
      }
    });
  }
});
