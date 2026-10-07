document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch and insert HTML components
    const loadComponent = (selector, url) => {
        fetch(url)
            .then(response => response.text())
            .then(data => {
                document.querySelector(selector).innerHTML = data;
                // After loading the header, re-attach the hamburger menu logic
                if (selector === '#header-placeholder') {
                    attachHamburgerLogic();
                }
            })
            .catch(error => console.error(`Error loading component from ${url}:`, error));
    };

    // Load header and footer
    loadComponent("#header-placeholder", "components/nav.html");
    loadComponent("#footer-placeholder", "components/footer.html");

    // Function to attach event listeners for the hamburger menu
    // This needs to be called *after* the header is loaded
    const attachHamburgerLogic = () => {
        const hamburger = document.getElementById('hamburger');
        const mobileNav = document.getElementById('mobile-nav');

        if (hamburger && mobileNav) {
            hamburger.addEventListener('click', function() {
                mobileNav.classList.toggle('active');
                const icon = hamburger.querySelector('i');
                if (mobileNav.classList.contains('active')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            });
        }
    };
});

// Modal functionality
                function openModal(modalId) {
                    document.getElementById(modalId).style.display = "block";
                }
                function closeModal(modalId) {
                    document.getElementById(modalId).style.display = "none";
                }
                window.onclick = function(event) {
                    if (event.target.className === 'modal') {
                        event.target.style.display = "none";
                    }
                }
                // Form submission handling