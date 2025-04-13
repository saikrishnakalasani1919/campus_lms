// Campus Bridge JavaScript functionality

document.addEventListener('DOMContentLoaded', function () {
  // Navbar scroll effect
  const navbar = document.querySelector('.navbar');

  window.addEventListener('scroll', function () {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // Scroll reveal animation for sections
  const sections = document.querySelectorAll('.about-section, .courses-section');

  // Initial check on load
  checkSections();

  // Check on scroll
  window.addEventListener('scroll', checkSections);

  function checkSections() {
    const triggerBottom = window.innerHeight * 0.8;

    sections.forEach(section => {
      const sectionTop = section.getBoundingClientRect().top;

      if (sectionTop < triggerBottom) {
        section.classList.add('visible');
      }
    });
  }

  // Add floating animation effect to course cards
  const courseCards = document.querySelectorAll('.course-card');

  courseCards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.2}s`;
    card.classList.add('floating');
  });

  // Smooth scrolling for navigation links
  const learnMoreBtn = document.querySelector('.btn-learn');

  if (learnMoreBtn) {
    learnMoreBtn.addEventListener('click', function (e) {
      e.preventDefault();

      const targetId = this.getAttribute('href');
      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        window.scrollTo({
          top: targetSection.offsetTop,
          behavior: 'smooth'
        });
      }
    });
  }

  // Dynamic Copyright Year
  const copyrightYear = document.querySelector('footer p');
  const currentYear = new Date().getFullYear();
  if (copyrightYear) {
    copyrightYear.innerHTML = `&copy; ${currentYear} <span class="footer-highlight">Campus Bridge</span>. All rights reserved.`;
  }

  // Add typing animation to hero heading
  const heroHeading = document.querySelector('.hero-content h1');
  if (heroHeading && window.innerWidth > 768) {
    const originalText = heroHeading.textContent;
    heroHeading.textContent = '';

    let charIndex = 0;
    const typingSpeed = 70;

    function typeText() {
      if (charIndex < originalText.length) {
        heroHeading.textContent += originalText.charAt(charIndex);
        charIndex++;
        setTimeout(typeText, typingSpeed);
      }
    }

    setTimeout(typeText, 500);
  }

  // Add hover effect to navigation buttons
  const navButtons = document.querySelectorAll('.nav-links .btn');

  navButtons.forEach(button => {
    button.addEventListener('mouseenter', function () {
      this.style.transform = 'translateY(-3px)';
    });

    button.addEventListener('mouseleave', function () {
      this.style.transform = 'translateY(0)';
    });
  });
});

// Optional: Add a simple preloader
window.addEventListener('load', function () {
  const preloader = document.createElement('div');
  preloader.className = 'preloader';
  preloader.innerHTML = `
    <style>
      .preloader {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        transition: opacity 0.5s ease, visibility 0.5s ease;
      }
      .loader {
        width: 50px;
        height: 50px;
        border: 5px solid #f3f3f3;
        border-top: 5px solid #3563E9;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    </style>
    <div class="loader"></div>
  `;

  document.body.appendChild(preloader);

  setTimeout(function () {
    preloader.style.opacity = '0';
    preloader.style.visibility = 'hidden';

    setTimeout(function () {
      document.body.removeChild(preloader);
    }, 500);
  }, 800);
});
