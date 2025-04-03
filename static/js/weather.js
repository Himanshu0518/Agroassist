document.addEventListener('DOMContentLoaded', function() {
  // Tab functionality
  const todayBtn = document.getElementById('todayBtn');
  const forecastBtn = document.getElementById('forecastBtn');
  const todaySection = document.getElementById('today_weather');
  const forecastSection = document.getElementById('forecast');

  // Initialize - hide forecast section
  forecastSection.classList.remove('active');
  todaySection.classList.add('active');
  
  // Update active class on tabs
  todayBtn.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Update active class on navigation
      todayBtn.parentElement.classList.add('active');
      forecastBtn.parentElement.classList.remove('active');
      
      // Show/hide appropriate sections with smooth transition
      forecastSection.classList.remove('active');
      
      // Small delay to ensure proper animation
      setTimeout(() => {
          todaySection.classList.add('active');
      }, 50);
  });
  
  forecastBtn.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Update active class on navigation
      forecastBtn.parentElement.classList.add('active');
      todayBtn.parentElement.classList.remove('active');
      
      // Show/hide appropriate sections with smooth transition
      todaySection.classList.remove('active');
      
      // Small delay to ensure proper animation
      setTimeout(() => {
          forecastSection.classList.add('active');
      }, 50);
  });

  // Forecast collapse functionality
  const forecastHeaders = document.querySelectorAll('.forecast-header');
  
  forecastHeaders.forEach(header => {
      header.addEventListener('click', function() {
          // Toggle aria-expanded attribute for icon rotation
          const isExpanded = this.getAttribute('aria-expanded') === 'true';
          this.setAttribute('aria-expanded', !isExpanded);
      });
  });

  // Background images based on weather conditions
  const setBackgroundBasedOnWeather = () => {
      const weatherDescription = document.querySelector('.weather-description');
      if (!weatherDescription) return;
      
      const weatherText = weatherDescription.textContent.toLowerCase();
      let backgroundImage;
      
      if (weatherText.includes('clear') || weatherText.includes('sun')) {
          backgroundImage = 'linear-gradient(135deg, #f6d365, #fda085)';
      } else if (weatherText.includes('cloud')) {
          backgroundImage = 'linear-gradient(135deg, #8BC6EC, #9599E2)';
      } else if (weatherText.includes('rain') || weatherText.includes('drizzle')) {
          backgroundImage = 'linear-gradient(135deg, #616161, #9bc5c3)';
      } else if (weatherText.includes('thunder') || weatherText.includes('storm')) {
          backgroundImage = 'linear-gradient(135deg, #133553, #393e46)';
      } else if (weatherText.includes('snow')) {
          backgroundImage = 'linear-gradient(135deg, #e6e9f0, #eef1f5)';
      } else if (weatherText.includes('mist') || weatherText.includes('fog')) {
          backgroundImage = 'linear-gradient(135deg, #b8d3fe, #aed8ec)';
      } else {
          // Default background
          backgroundImage = 'linear-gradient(135deg, #6dd5ed, #2193b0)';
      }
      
      document.body.style.background = backgroundImage;
      document.body.style.backgroundSize = 'cover';
      document.body.style.backgroundAttachment = 'fixed';
  };
  
  // Apply weather-based background
  setBackgroundBasedOnWeather();

  // Add animation to weather details
  const animateElements = () => {
      const weatherCard = document.querySelector('.current-weather');
      const forecastCards = document.querySelectorAll('.forecast-card');
      
      if (weatherCard) {
          weatherCard.classList.add('animate-in');
      }
      
      if (forecastCards.length > 0) {
          forecastCards.forEach((card, index) => {
              setTimeout(() => {
                  card.classList.add('animate-in');
              }, 100 * index);
          });
      }
  };
  
  // Trigger animations after a small delay
  setTimeout(animateElements, 300);

  // Add smooth scrolling to all links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
          e.preventDefault();
          
          document.querySelector(this.getAttribute('href')).scrollIntoView({
              behavior: 'smooth'
          });
      });
  });

  // Add keyframe animations via CSS
  const styleSheet = document.createElement('style');
  styleSheet.type = 'text/css';
  styleSheet.innerHTML = `
      @keyframes fadeInUp {
          from {
              opacity: 0;
              transform: translateY(20px);
          }
          to {
              opacity: 1;
              transform: translateY(0);
          }
      }
      
      .animate-in {
          animation: fadeInUp 0.5s ease forwards;
      }
      
      .weather-section.active {
          animation: fadeIn 0.5s ease forwards;
      }
      
      @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
      }
  `;
  document.head.appendChild(styleSheet);

  // Make hourly forecast scrollable with buttons
  const createScrollButtons = () => {
      const hourlyContainers = document.querySelectorAll('.hourly-container');
      
      hourlyContainers.forEach(container => {
          // Create scroll buttons
          const scrollLeftBtn = document.createElement('button');
          scrollLeftBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
          scrollLeftBtn.className = 'scroll-btn scroll-left';
          
          const scrollRightBtn = document.createElement('button');
          scrollRightBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
          scrollRightBtn.className = 'scroll-btn scroll-right';
          
          // Add event listeners
          scrollLeftBtn.addEventListener('click', () => {
              container.scrollBy({ left: -200, behavior: 'smooth' });
          });
          
          scrollRightBtn.addEventListener('click', () => {
              container.scrollBy({ left: 200, behavior: 'smooth' });
          });
          
          // Add buttons to parent
          const parent = container.parentElement;
          parent.style.position = 'relative';
          parent.appendChild(scrollLeftBtn);
          parent.appendChild(scrollRightBtn);
      });
      
      // Add CSS for scroll buttons
      const scrollBtnStyle = document.createElement('style');
      scrollBtnStyle.innerHTML = `
          .scroll-btn {
              position: absolute;
              top: 50%;
              transform: translateY(-50%);
              width: 40px;
              height: 40px;
              border-radius: 50%;
              background: rgba(255, 255, 255, 0.8);
              border: none;
              box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
              cursor: pointer;
              z-index: 10;
              display: flex;
              align-items: center;
              justify-content: center;
              transition: all 0.3s ease;
          }
          
          .scroll-btn:hover {
              background: white;
              box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
          }
          
          .scroll-left {
              left: 10px;
          }
          
          .scroll-right {
              right: 10px;
          }
      `;
      document.head.appendChild(scrollBtnStyle);
  };
  
  // Add scroll buttons with a delay to ensure elements are rendered
  setTimeout(createScrollButtons, 500);
});