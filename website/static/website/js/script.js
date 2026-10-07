/* ============================================================
   NiiKpakpo — Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Scroll-aware navigation ─────────────────────────────────
  const nav = document.getElementById('nav');
  if (nav) {
    const isInnerPage = nav.classList.contains('is-scrolled');
    const updateNav = () => {
      if (!isInnerPage) {
        nav.classList.toggle('is-scrolled', window.scrollY > 60);
      }
    };
    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();
  }

  // ── Hamburger / mobile drawer ───────────────────────────────
  const hamburger = document.getElementById('hamburger');
  const drawer    = document.getElementById('drawer');
  if (hamburger && drawer) {
    hamburger.addEventListener('click', () => {
      const open = drawer.classList.toggle('is-open');
      hamburger.classList.toggle('is-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    drawer.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        drawer.classList.remove('is-open');
        hamburger.classList.remove('is-open');
        document.body.style.overflow = '';
      });
    });
  }

  // ── Scroll reveal (IntersectionObserver) ───────────────────
  const revealEls = document.querySelectorAll('[data-reveal]');
  if (revealEls.length) {
    const revealObserver = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    revealEls.forEach(el => revealObserver.observe(el));
  }

  // ── Smooth scroll for in-page anchor links ──────────────────
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    const href = a.getAttribute('href');
    if (href === '#') return;
    a.addEventListener('click', e => {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const navH = nav ? nav.offsetHeight : 80;
        const top  = target.getBoundingClientRect().top + window.scrollY - navH - 24;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  // ── Stats counter animation ─────────────────────────────────
  const statNumbers = document.querySelectorAll('[data-target]');
  if (statNumbers.length) {
    const easeOut = t => 1 - Math.pow(1 - t, 3);
    const animateCounter = (el, target, duration = 1800) => {
      const start = performance.now();
      const update = now => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        el.textContent = Math.round(easeOut(progress) * target).toLocaleString();
        if (progress < 1) requestAnimationFrame(update);
      };
      requestAnimationFrame(update);
    };

    const counterObserver = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const el = entry.target;
            animateCounter(el, parseInt(el.dataset.target, 10));
            counterObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );
    statNumbers.forEach(el => counterObserver.observe(el));
  }

  // ── Blog category filter ────────────────────────────────────
  const filterBtns       = document.querySelectorAll('.filter-btn');
  const sidebarItems     = document.querySelectorAll('.sidebar-filter-item');
  const postCards        = document.querySelectorAll('.post-card');
  const noResults        = document.getElementById('no-results');

  if (filterBtns.length && postCards.length) {

    const applyFilter = category => {
      let visible = 0;

      postCards.forEach(card => {
        const match = category === 'all' || card.dataset.category === category;
        card.style.display = match ? '' : 'none';
        if (match) visible++;
      });

      if (noResults) noResults.style.display = visible === 0 ? 'block' : 'none';

      // Sync filter bar
      filterBtns.forEach(btn =>
        btn.classList.toggle('active', btn.dataset.category === category)
      );

      // Sync sidebar
      sidebarItems.forEach(item =>
        item.classList.toggle('active-cat', item.dataset.category === category)
      );
    };

    // Filter bar buttons
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => applyFilter(btn.dataset.category));
    });

    // Sidebar category items (prevent page jump)
    sidebarItems.forEach(item => {
      item.addEventListener('click', e => {
        e.preventDefault();
        applyFilter(item.dataset.category);
        // Scroll to top of posts smoothly
        const postsEl = document.querySelector('.blog-posts');
        if (postsEl) {
          const navH = nav ? nav.offsetHeight : 80;
          const top  = postsEl.getBoundingClientRect().top + window.scrollY - navH - 24;
          window.scrollTo({ top, behavior: 'smooth' });
        }
      });
    });
  }

});
