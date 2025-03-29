// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Get location button functionality
    document.getElementById('get-location').addEventListener('click', function() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          document.getElementById('latitude').value = position.coords.latitude.toFixed(6);
          document.getElementById('longitude').value = position.coords.longitude.toFixed(6);
        }, function(error) {
          alert('Error getting location: ' + error.message);
        });
      } else {
        alert('Geolocation is not supported by this browser.');
      }
    });
    
    // Form submission animation
    document.getElementById('recommendation-form').addEventListener('submit', function() {
      document.getElementById('loading').classList.remove('d-none');
    });
    
    // Add tooltips using Bootstrap or a simple title attribute
    const tooltips = document.querySelectorAll('.tooltip-icon');
    tooltips.forEach(function(tooltip) {
      const title = tooltip.getAttribute('title');
      tooltip.setAttribute('data-bs-toggle', 'tooltip');
      tooltip.setAttribute('data-bs-placement', 'top');
    });
    
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
      const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
      });
    }
  });