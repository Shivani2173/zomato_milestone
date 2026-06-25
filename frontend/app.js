/**
 * app.js — Zomato AI Restaurant Recommender
 * Handles: API status check, dropdown population, form submission,
 * skeleton loading, card rendering, toast notifications, clear filters.
 */

// Auto-detect environment: use Render backend in production, localhost in dev
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000'
  : 'https://zomato-milestone-t73o.onrender.com';

// ─── Element refs ────────────────────────────────────────────────────────────
const apiStatusEl    = document.getElementById('api-status');
const statusDot      = apiStatusEl.querySelector('.status-dot');
const statusLabel    = apiStatusEl.querySelector('.status-label');

const locationSelect = document.getElementById('location');
const cuisineSelect  = document.getElementById('cuisine');
const budgetInput    = document.getElementById('budget-value');
const ratingSlider   = document.getElementById('min-rating');
const ratingDisplay  = document.getElementById('rating-display');
const notesArea      = document.getElementById('notes');
const charCount      = document.getElementById('char-count');

const submitBtn      = document.getElementById('submit-btn');
const btnContent     = submitBtn.querySelector('.btn-content');
const btnSpinner     = submitBtn.querySelector('.btn-spinner');
const clearBtn       = document.getElementById('clear-btn');
const form           = document.getElementById('recommend-form');

const locationError  = document.getElementById('location-error');

const emptyState     = document.getElementById('results-empty');
const skeletonState  = document.getElementById('results-skeletons');
const zeroState      = document.getElementById('results-zero');
const cardsContainer = document.getElementById('results-cards');

const toastContainer = document.getElementById('toast-container');

// ─── Utility: show/hide results panels ───────────────────────────────────────
function showPanel(which) {
  emptyState.classList.add('hidden');
  skeletonState.classList.add('hidden');
  zeroState.classList.add('hidden');
  cardsContainer.classList.add('hidden');

  if (which === 'empty')    emptyState.classList.remove('hidden');
  if (which === 'skeleton') skeletonState.classList.remove('hidden');
  if (which === 'zero')     zeroState.classList.remove('hidden');
  if (which === 'cards')    cardsContainer.classList.remove('hidden');
}

// ─── Toast system ─────────────────────────────────────────────────────────────
function showToast(message, type = 'info', duration = 4000) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => toast.remove(), 450);
  }, duration);
}

// ─── API status check ─────────────────────────────────────────────────────────
async function checkApiStatus() {
  try {
    const res = await fetch(`${API_BASE}/`, { signal: AbortSignal.timeout(4000) });
    if (res.ok) {
      apiStatusEl.classList.add('connected');
      apiStatusEl.classList.remove('offline');
      statusLabel.textContent = 'API Connected';
    } else { setOffline(); }
  } catch {
    setOffline();
  }
}

function setOffline() {
  apiStatusEl.classList.add('offline');
  apiStatusEl.classList.remove('connected');
  statusLabel.textContent = 'API Offline';
}

// ─── Populate Location dropdown ───────────────────────────────────────────────
async function loadLocations() {
  try {
    const res  = await fetch(`${API_BASE}/api/locations`);
    const data = await res.json();
    data.locations.forEach(loc => {
      const opt = document.createElement('option');
      opt.value = loc;
      opt.textContent = loc;
      locationSelect.appendChild(opt);
    });
  } catch {
    showToast('Could not load locations. Is the backend running?', 'error');
  }
}

// ─── Populate Cuisine dropdown ────────────────────────────────────────────────
async function loadCuisines() {
  try {
    const res  = await fetch(`${API_BASE}/api/cuisines`);
    const data = await res.json();
    data.cuisines.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c;
      opt.textContent = c;
      cuisineSelect.appendChild(opt);
    });
  } catch {
    showToast('Could not load cuisines. Is the backend running?', 'error');
  }
}

// ─── Budget toggle ────────────────────────────────────────────────────────────
document.querySelectorAll('.budget-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.budget-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    budgetInput.value = btn.dataset.value;
  });
});

// ─── Rating slider ────────────────────────────────────────────────────────────
ratingSlider.addEventListener('input', () => {
  const val = parseFloat(ratingSlider.value);
  ratingDisplay.textContent = `${val}+`;

  // Gradient fill effect on the track
  const pct = (val / 5) * 100;
  ratingSlider.style.background =
    `linear-gradient(to right, var(--accent-start) 0%, var(--accent-end) ${pct}%, var(--surface-high) ${pct}%)`;
});

// Trigger on load to set initial gradient
ratingSlider.dispatchEvent(new Event('input'));

// ─── Textarea char counter ────────────────────────────────────────────────────
notesArea.addEventListener('input', () => {
  charCount.textContent = `${notesArea.value.length} / 200`;
});

// ─── Build recommendation card DOM ────────────────────────────────────────────
function buildCard(rec, index) {
  const card = document.createElement('article');
  card.className = 'rec-card';
  card.setAttribute('aria-label', `Recommendation ${index + 1}: ${rec.name}`);

  const rank = document.createElement('div');
  rank.className = 'rank-badge';
  rank.textContent = `#${index + 1}`;

  const header = document.createElement('div');
  header.className = 'card-header';

  const name = document.createElement('h2');
  name.className = 'card-name';
  name.textContent = rec.name;

  const rating = document.createElement('span');
  rating.className = 'card-rating';
  rating.textContent = `⭐ ${rec.rating.toFixed(1)}`;

  header.appendChild(name);
  header.appendChild(rating);

  const tags = document.createElement('div');
  tags.className = 'card-tags';

  if (rec.cuisine) {
    const ct = document.createElement('span');
    ct.className = 'tag tag-cuisine';
    ct.textContent = `🍜 ${rec.cuisine}`;
    tags.appendChild(ct);
  }

  if (rec.estimated_cost) {
    const costTag = document.createElement('span');
    costTag.className = 'tag tag-cost';
    costTag.textContent = `₹ ${rec.estimated_cost.toLocaleString('en-IN')} for two`;
    tags.appendChild(costTag);
  }

  const aiLabel = document.createElement('p');
  aiLabel.className = 'card-ai-label';
  aiLabel.textContent = '🤖 AI says —';

  const aiText = document.createElement('p');
  aiText.className = 'card-ai-text';
  aiText.textContent = rec.ai_explanation;

  card.appendChild(rank);
  card.appendChild(header);
  card.appendChild(tags);
  card.appendChild(aiLabel);
  card.appendChild(aiText);

  return card;
}

// ─── Form submission ──────────────────────────────────────────────────────────
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Validate location
  if (!locationSelect.value) {
    locationError.classList.remove('hidden');
    locationSelect.focus();
    return;
  }
  locationError.classList.add('hidden');

  // Build payload
  const payload = {
    location:   locationSelect.value,
    cuisine:    cuisineSelect.value || null,
    budget:     budgetInput.value   || null,
    min_rating: parseFloat(ratingSlider.value),
    notes:      notesArea.value.trim()
  };

  // Loading state
  btnContent.classList.add('hidden');
  btnSpinner.classList.remove('hidden');
  submitBtn.disabled = true;
  showPanel('skeleton');

  try {
    const res = await fetch(`${API_BASE}/api/recommend`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);

    const data = await res.json();

    if (!data.success || data.count === 0) {
      showPanel('zero');
      if (data.message) showToast(data.message, 'info');
    } else {
      cardsContainer.innerHTML = '';
      data.recommendations.forEach((rec, i) => {
        cardsContainer.appendChild(buildCard(rec, i));
      });
      showPanel('cards');
      showToast(`Found ${data.count} great match${data.count > 1 ? 'es' : ''}!`, 'success');
    }

  } catch (err) {
    showPanel('empty');
    showToast('Something went wrong. Is the backend running?', 'error');
    console.error('[Recommend Error]', err);
  } finally {
    btnContent.classList.remove('hidden');
    btnSpinner.classList.add('hidden');
    submitBtn.disabled = false;
  }
});

// ─── Clear filters ────────────────────────────────────────────────────────────
clearBtn.addEventListener('click', () => {
  locationSelect.value = '';
  cuisineSelect.value  = '';
  budgetInput.value    = 'low';

  document.querySelectorAll('.budget-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('budget-low').classList.add('active');

  ratingSlider.value = '3.5';
  ratingSlider.dispatchEvent(new Event('input'));

  notesArea.value    = '';
  charCount.textContent = '0 / 200';
  locationError.classList.add('hidden');

  cardsContainer.innerHTML = '';
  showPanel('empty');
});

// ─── Initialise on page load ──────────────────────────────────────────────────
(async function init() {
  await Promise.all([
    checkApiStatus(),
    loadLocations(),
    loadCuisines()
  ]);
})();
