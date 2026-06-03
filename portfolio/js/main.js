(function () {
    var root = document.documentElement;
    var navToggle = document.querySelector('.nav-toggle');
    var navLinks = document.querySelector('.nav-links');
    var navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');
    var themeToggle = document.querySelector('.theme-toggle');
    var themeToggleText = document.querySelector('.theme-toggle-text');
    var currentYear = document.getElementById('current-year');
    var revealItems = document.querySelectorAll('.reveal');
    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function getPreferredTheme() {
        try {
            var storedTheme = window.localStorage.getItem('portfolio-theme');
            if (storedTheme === 'light' || storedTheme === 'dark') {
                return storedTheme;
            }
        } catch (error) {
            return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }

        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function setTheme(theme) {
        root.setAttribute('data-theme', theme);

        if (themeToggleText) {
            themeToggleText.textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
        }

        if (themeToggle) {
            themeToggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
        }

        try {
            window.localStorage.setItem('portfolio-theme', theme);
        } catch (error) {
            return;
        }
    }

    function closeMenu() {
        if (!navToggle || !navLinks) {
            return;
        }

        navLinks.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Open navigation menu');
    }

    function toggleMenu() {
        if (!navToggle || !navLinks) {
            return;
        }

        var isOpen = navLinks.classList.toggle('is-open');
        navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        navToggle.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
    }

    function handleAnchorClick(event) {
        var targetId = event.currentTarget.getAttribute('href');
        var target = document.querySelector(targetId);

        if (!target) {
            return;
        }

        event.preventDefault();
        closeMenu();

        if (typeof target.scrollIntoView === 'function' && !reducedMotion) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            window.location.hash = targetId;
        }
    }

    function showElements() {
        var index;
        for (index = 0; index < revealItems.length; index += 1) {
            revealItems[index].classList.add('is-visible');
        }
    }

    function enableReveal() {
        if (!('IntersectionObserver' in window) || reducedMotion) {
            showElements();
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            var index;
            for (index = 0; index < entries.length; index += 1) {
                if (entries[index].isIntersecting) {
                    entries[index].target.classList.add('is-visible');
                    observer.unobserve(entries[index].target);
                }
            }
        }, {
            threshold: 0.15
        });

        var itemIndex;
        for (itemIndex = 0; itemIndex < revealItems.length; itemIndex += 1) {
            observer.observe(revealItems[itemIndex]);
        }
    }

    if (navToggle) {
        navToggle.addEventListener('click', toggleMenu);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var nextTheme = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            setTheme(nextTheme);
        });
    }

    var linkIndex;
    for (linkIndex = 0; linkIndex < navAnchors.length; linkIndex += 1) {
        navAnchors[linkIndex].addEventListener('click', handleAnchorClick);
    }

    document.addEventListener('click', function (event) {
        if (!navLinks || !navToggle) {
            return;
        }

        if (!navLinks.contains(event.target) && !navToggle.contains(event.target) && navLinks.classList.contains('is-open')) {
            closeMenu();
        }
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth >= 900) {
            closeMenu();
        }
    });

    if (currentYear) {
        currentYear.textContent = String(new Date().getFullYear());
    }

    setTheme(getPreferredTheme());
    enableReveal();
}());
