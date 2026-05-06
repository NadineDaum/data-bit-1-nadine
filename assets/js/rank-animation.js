(function () {
    const MAX_VISIBLE_ROWS = 7;
    const AUTOPLAY_MS = 4600;

    document.addEventListener('DOMContentLoaded', initRankAnimation);

    function initRankAnimation() {
        const root = document.querySelector('[data-rank-animation]');
        const stack = document.querySelector('[data-rank-stack]');

        if (!root || !stack || typeof countriesDataInline === 'undefined') {
            return;
        }

        const controls = Array.from(root.querySelectorAll('[data-rank-mode]'));
        const eyebrow = root.querySelector('[data-rank-eyebrow]');
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        let mode = 'gains';
        let timer = null;

        const render = (nextMode) => {
            mode = nextMode;
            root.dataset.mode = mode;
            updateControls(controls, mode);

            if (eyebrow) {
                eyebrow.textContent = mode === 'gains' ? 'Biggest gains' : 'Biggest declines';
            }

            const countries = getRankedCountries(mode);
            const largestMagnitude = Math.max(...countries.map(country => Math.abs(country.change)));

            stack.replaceChildren(...countries.map((country, index) => {
                const row = document.createElement('li');
                const changeSign = country.change >= 0 ? '+' : '';
                const magnitude = Math.abs(country.change) / largestMagnitude;

                row.className = 'rank-animation__row';
                row.style.setProperty('--row-delay', `${index * 46}ms`);
                row.style.setProperty('--row-scale', Math.max(0.12, magnitude).toFixed(2));
                row.innerHTML = `
                    <span class="rank-animation__rank">${String(index + 1).padStart(2, '0')}</span>
                    <span class="rank-animation__country">${country.country}</span>
                    <span class="rank-animation__change">${changeSign}${country.change.toFixed(1)}</span>
                `;

                return row;
            }));
        };

        const restartAutoplay = () => {
            if (prefersReducedMotion) return;
            window.clearInterval(timer);
            timer = window.setInterval(() => {
                render(mode === 'gains' ? 'declines' : 'gains');
            }, AUTOPLAY_MS);
        };

        controls.forEach(button => {
            button.addEventListener('click', () => {
                render(button.dataset.rankMode);
                restartAutoplay();
            });
        });

        render(mode);
        restartAutoplay();
    }

    function getRankedCountries(mode) {
        return [...countriesDataInline]
            .sort((a, b) => mode === 'gains' ? b.change - a.change : a.change - b.change)
            .slice(0, MAX_VISIBLE_ROWS);
    }

    function updateControls(controls, mode) {
        controls.forEach(button => {
            const isActive = button.dataset.rankMode === mode;
            button.classList.toggle('is-active', isActive);
            button.setAttribute('aria-pressed', String(isActive));
        });
    }
})();
