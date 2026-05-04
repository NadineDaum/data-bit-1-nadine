/**
 * Scrollytelling Navigation & Interactions
 */

// Track which section is currently in view
document.addEventListener('DOMContentLoaded', function () {
    setupNavigation();
    setupScrollSpyObserver();
    setupViewToggle();
});

/**
 * Setup smooth scroll navigation
 */
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                    // Update active state
                    updateActiveNavLink(href);
                }
            }
        });
    });
}

/**
 * Intersection Observer for scroll-based nav highlighting
 */
function setupScrollSpyObserver() {
    const sections = document.querySelectorAll('[id^="section-"]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sectionId = '#' + entry.target.id;
                updateActiveNavLink(sectionId);
            }
        });
    }, {
        threshold: 0.4,
        rootMargin: '-100px 0px -100px 0px'
    });

    sections.forEach(section => observer.observe(section));
}

/**
 * Update active nav link
 */
function updateActiveNavLink(sectionId) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === sectionId) {
            link.classList.add('active');
        }
    });
}

/**
 * Add animation to nav when scrolling
 */
window.addEventListener('scroll', function () {
    const nav = document.querySelector('.sticky-nav');
    if (window.scrollY > 100) {
        nav.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
    } else {
        nav.style.boxShadow = 'none';
    }
});

/**
 * Setup year slider sync
 */
function setupYearSlider() {
    const yearSlider = document.querySelector('[data-year-slider]');
    const yearLabel = document.querySelector('[data-year-label]');

    if (yearSlider && yearLabel) {
        const syncYear = () => {
            yearLabel.textContent = yearSlider.value;
        };

        yearSlider.addEventListener('input', syncYear);
        syncYear();
    }
}

/**
 * Setup view toggle (Map vs List)
 */
let countriesData = [];
let currentSortOrder = 'asc'; // Default sort order

function setupViewToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-tab');
    const mapView = document.getElementById('map-view');
    const listView = document.getElementById('list-view');
    const sortButtons = document.querySelectorAll('.sort-btn');

    // Load countries data
    loadCountriesData().then(() => {
        populateTable(currentSortOrder);
    });

    // Toggle buttons
    toggleButtons.forEach(button => {
        button.addEventListener('click', function () {
            const view = this.getAttribute('data-view');

            // Update active button
            toggleButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Show/hide views
            if (view === 'map') {
                mapView.style.display = 'block';
                listView.style.display = 'none';
            } else {
                mapView.style.display = 'none';
                listView.style.display = 'block';
            }
        });
    });

    // Sort buttons
    sortButtons.forEach(button => {
        button.addEventListener('click', function () {
            const sortOrder = this.getAttribute('data-sort');

            // Update active button
            sortButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Update sort and refresh table
            currentSortOrder = sortOrder;
            populateTable(sortOrder);
        });
    });
}

/**
 * Load countries data from inline variable
 */
function loadCountriesData() {
    return new Promise((resolve) => {
        if (typeof countriesDataInline !== 'undefined' && countriesDataInline.length > 0) {
            countriesData = countriesDataInline;
            console.log('Loaded', countriesData.length, 'countries');
            resolve();
        } else {
            console.error('Countries data not found');
            resolve();
        }
    });
}

/**
 * Populate the table with sorted countries data
 */
function populateTable(sortOrder) {
    const tableBody = document.getElementById('table-body');
    if (!tableBody || !countriesData || countriesData.length === 0) return;

    // Sort the data
    let sortedData = [...countriesData];

    if (sortOrder === 'asc') {
        sortedData.sort((a, b) => a.change - b.change);
    } else {
        sortedData.sort((a, b) => b.change - a.change);
    }

    // Clear table
    tableBody.innerHTML = '';

    // Populate with sorted data
    sortedData.forEach(country => {
        const row = document.createElement('tr');

        const changeClass = country.change >= 0 ? 'change-positive' : 'change-negative';
        const changeSign = country.change >= 0 ? '+' : '';

        row.innerHTML = `
            <td>${country.country}</td>
            <td>${country.score_2015.toFixed(2)}</td>
            <td>${country.score_2025.toFixed(2)}</td>
            <td class="change-cell ${changeClass}">${changeSign}${country.change.toFixed(2)}</td>
        `;

        tableBody.appendChild(row);
    });
}
