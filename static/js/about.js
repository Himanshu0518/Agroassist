document.addEventListener('DOMContentLoaded', function() {
    // Animate elements when they come into view
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.feature-card, .tech-card, .about-image-container, .about-content, .data-step');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animate-fadeIn');
                element.style.opacity = '1';
            }
        });
    };
    
    // Set initial state for elements
    const elementsToAnimate = document.querySelectorAll('.feature-card, .tech-card, .about-image-container, .about-content, .data-step');
    elementsToAnimate.forEach(element => {
        element.style.opacity = '0';
    });
    
    // Run animation check on load and scroll
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === "#") return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Add offset for fixed header if necessary
                const offset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Interactive data flow
    const dataSteps = document.querySelectorAll('.data-step');
    dataSteps.forEach((step, index) => {
        step.addEventListener('mouseenter', () => {
            step.style.transform = 'scale(1.05)';
            
            // Highlight the current step
            dataSteps.forEach((s, i) => {
                if (i <= index) {
                    s.style.backgroundColor = '#e8f5e9';
                    s.style.borderColor = '#28a745';
                } else {
                    s.style.backgroundColor = '#f8f9fa';
                    s.style.borderColor = '#eee';
                }
            });
        });
        
        step.addEventListener('mouseleave', () => {
            step.style.transform = '';
            
            // Reset all steps
            dataSteps.forEach(s => {
                s.style.backgroundColor = '#f8f9fa';
                s.style.borderColor = '#eee';
            });
        });
    });
    
    // Counter animation for stats
    const animateCounter = (element, start, end, duration) => {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const currentCount = Math.floor(progress * (end - start) + start);
            element.textContent = currentCount;
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                element.textContent = end;
            }
        };
        window.requestAnimationFrame(step);
    };
    
    // Function to check if element is in viewport
    const isInViewport = (element) => {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    };
    
    // Initialize parallax effect on about image
    const aboutImage = document.querySelector('.about-image-container');
    if (aboutImage) {
        window.addEventListener('scroll', () => {
            const scrollPosition = window.pageYOffset;
            const shapes = document.querySelectorAll('.shape-accent');
            
            shapes.forEach((shape, index) => {
                const speed = 0.05 * (index + 1);
                shape.style.transform = `translate(${20 + scrollPosition * speed}px, ${20 + scrollPosition * speed}px)`;
            });
        });
    }
    
    // Feature card enhanced interaction
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            const img = card.querySelector('img');
            if (img) {
                img.style.transform = 'scale(1.1)';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            const img = card.querySelector('img');
            if (img) {
                img.style.transform = '';
            }
        });
    });
});