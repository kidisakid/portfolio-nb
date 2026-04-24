/* Portfolio · interactions
   - Scroll progress bar
   - Nav scroll state
   - Parallax layers (rAF-driven, throttled)
   - 3D mouse-tracking tilt
   - Intersection-observer reveals
   - Reduced-motion respect
*/
(() => {
  'use strict';

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── Scroll progress + nav scrolled state ──────────────────────────
  const progressBar = document.getElementById('scroll-progress-bar');
  const nav = document.getElementById('nav');

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const doc = document.documentElement;
      const scrollTop = doc.scrollTop || document.body.scrollTop;
      const height = doc.scrollHeight - doc.clientHeight;
      const pct = height > 0 ? (scrollTop / height) * 100 : 0;
      if (progressBar) progressBar.style.width = pct + '%';

      if (nav) {
        nav.classList.toggle('scrolled', scrollTop > 40);
      }

      if (!prefersReduced) applyParallax(scrollTop);

      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  // ── Parallax ──────────────────────────────────────────────────────
  const parallaxEls = Array.from(document.querySelectorAll('[data-parallax-speed]'))
    .map(el => ({
      el,
      speed: parseFloat(el.dataset.parallaxSpeed) || 0.2,
    }));

  function applyParallax(scrollTop) {
    for (const { el, speed } of parallaxEls) {
      const rect = el.getBoundingClientRect();
      const viewportH = window.innerHeight;
      if (rect.bottom < -200 || rect.top > viewportH + 200) continue;
      const y = -scrollTop * speed;
      el.style.transform = `translate3d(0, ${y}px, 0)`;
    }
  }
  applyParallax(window.scrollY);

  // ── 3D tilt on mouse move ─────────────────────────────────────────
  if (!prefersReduced) {
    const tiltEls = document.querySelectorAll('[data-tilt]');
    tiltEls.forEach(el => {
      const MAX = 8; // degrees
      let raf = null;

      const onMove = (e) => {
        const rect = el.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const dx = (e.clientX - cx) / (rect.width / 2);
        const dy = (e.clientY - cy) / (rect.height / 2);
        const rotY = dx * MAX;
        const rotX = -dy * MAX;

        // animate transform on the first child with transform-style preserve-3d
        const target = el.querySelector('.portrait-frame, .cert-stack, .project-card-inner') || el;

        if (raf) cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          target.style.transform = `rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg)`;
        });
      };

      const onLeave = () => {
        const target = el.querySelector('.portrait-frame, .cert-stack, .project-card-inner') || el;
        if (raf) cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          target.style.transform = '';
        });
      };

      el.addEventListener('mousemove', onMove);
      el.addEventListener('mouseleave', onLeave);
    });
  }

  // ── Reveal on scroll ──────────────────────────────────────────────
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !prefersReduced) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px -5% 0px' });

    // stagger: small delay per element inside the same parent
    const groups = new Map();
    revealEls.forEach(el => {
      const parent = el.parentElement;
      if (!groups.has(parent)) groups.set(parent, []);
      groups.get(parent).push(el);
    });
    groups.forEach(list => {
      list.forEach((el, i) => {
        el.style.transitionDelay = Math.min(i * 70, 420) + 'ms';
        io.observe(el);
      });
    });

    // Edge case: hash-nav on load — reveal anything above the landing point
    // so users don't scroll up into blanked-out sections.
    const revealAbove = () => {
      const y = window.scrollY + window.innerHeight;
      revealEls.forEach(el => {
        const top = el.getBoundingClientRect().top + window.scrollY;
        if (top < y) el.classList.add('in-view');
      });
    };
    if (location.hash) {
      // browser handles the scroll; queue a reveal sweep after
      setTimeout(revealAbove, 50);
    }
    // belt-and-suspenders: on any anchor click, sweep above once scrolled
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', () => setTimeout(revealAbove, 700));
    });
  } else {
    revealEls.forEach(el => el.classList.add('in-view'));
  }

  // ── Streamlit iframe: hide loader when loaded ─────────────────────
  const iframe = document.querySelector('.embed-iframe');
  const loader = document.querySelector('.embed-loading');
  if (iframe && loader) {
    const hide = () => { loader.style.opacity = '0'; setTimeout(() => loader.style.display = 'none', 400); };
    iframe.addEventListener('load', hide);
    // safety: hide after 15s even if load event doesn't fire cross-origin
    setTimeout(hide, 15000);
  }

  // ── Hero title outline on initial reveal ──────────────────────────
  // (nothing extra — handled by CSS :hover)

  // Initial paint
  onScroll();
})();
