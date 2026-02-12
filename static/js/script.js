let slide = 0;

function nextSlide() {
    slide++;
    alert("Next slide " + slide);
}

function prevSlide() {
    slide--;
    alert("Previous slide " + slide);
}

// Interactive UI toggles (collapsible panels and model details)
document.addEventListener('DOMContentLoaded', function () {
    function toggleTarget(btn) {
        const selector = btn.getAttribute('data-target');
        if (!selector) return;
        const el = document.querySelector(selector);
        if (!el) return;
        const expanded = btn.getAttribute('aria-expanded') === 'true';
        if (expanded) {
            btn.setAttribute('aria-expanded', 'false');
            el.classList.remove('collapse-visible');
            el.classList.add('collapse-hidden');
            el.setAttribute('aria-hidden', 'true');
        } else {
            btn.setAttribute('aria-expanded', 'true');
            el.classList.remove('collapse-hidden');
            el.classList.add('collapse-visible');
            el.setAttribute('aria-hidden', 'false');
        }
        // remember state for this panel
        try { localStorage.setItem('panel:' + selector, btn.getAttribute('aria-expanded')); } catch (e) {}
    }

    document.querySelectorAll('.toggle-btn').forEach(function (btn) {
        const target = btn.getAttribute('data-target');
        // initialize from storage if found
        try {
            const saved = localStorage.getItem('panel:' + target);
            if (saved === 'true') {
                btn.setAttribute('aria-expanded', 'true');
                const el = document.querySelector(target);
                if (el) { el.classList.remove('collapse-hidden'); el.classList.add('collapse-visible'); el.setAttribute('aria-hidden', 'false'); }
            }
        } catch (e) {}

        btn.addEventListener('click', function (e) {
            e.preventDefault();
            toggleTarget(btn);
        });

        // allow Enter/Space keyboard activation
        btn.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleTarget(btn); }
        });
    });

    // Accessibility: allow clicking the legend area to toggle options-card
    document.querySelectorAll('.options-card legend').forEach(function (legend) {
        legend.addEventListener('click', function (e) {
            const btn = legend.querySelector('.toggle-btn');
            if (btn) { btn.click(); }
        });
    });

    // Hamburger Menu Toggle for Mobile Navigation
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navLinks = document.getElementById('navLinks');
    
    if (hamburgerBtn && navLinks) {
        hamburgerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            navLinks.classList.toggle('active');
            
            // Toggle icon between bars and times (X)
            const icon = hamburgerBtn.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
        
        // Close menu when clicking on a link
        navLinks.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                navLinks.classList.remove('active');
                const icon = hamburgerBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!hamburgerBtn.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                const icon = hamburgerBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
});
