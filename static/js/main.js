document.addEventListener("DOMContentLoaded", function () {
  // Get elements
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("sidebarToggle");
  const main = document.getElementById("main");
  
  // Toggle sidebar function
  function toggleSidebar() {
    sidebar.classList.toggle("closed");
    main.classList.toggle("expanded");
    
    // Change toggle button icon and position
    if (sidebar.classList.contains("closed")) {
      toggleBtn.querySelector("i").classList.remove("fa-times");
      toggleBtn.querySelector("i").classList.add("fa-bars");
      toggleBtn.style.left = "20px";
    } else {
      toggleBtn.querySelector("i").classList.remove("fa-bars");
      toggleBtn.querySelector("i").classList.add("fa-times");
      if (window.innerWidth > 768) {
        toggleBtn.style.left = "260px";
      }
    }
  }
  
  // Toggle sidebar on button click
  toggleBtn.addEventListener("click", toggleSidebar);
  
  // Responsive layout handler
  function handleResponsiveLayout() {
    if (window.innerWidth <= 768) {
      // For small screens
      sidebar.classList.add("closed");
      main.classList.add("expanded");
      toggleBtn.style.left = "20px";
      toggleBtn.querySelector("i").classList.remove("fa-times");
      toggleBtn.querySelector("i").classList.add("fa-bars");
    } else {
      // For larger screens
      sidebar.classList.remove("closed");
      main.classList.remove("expanded");
      toggleBtn.style.left = "260px";
      toggleBtn.querySelector("i").classList.remove("fa-times");
      toggleBtn.querySelector("i").classList.add("fa-bars");
    }
  }
  
  // Apply responsive layout on page load and resize
  window.addEventListener("resize", handleResponsiveLayout);
  handleResponsiveLayout();
  
  // Close sidebar when clicking outside on small screens
  document.addEventListener("click", function(event) {
    const isSmallScreen = window.innerWidth <= 768;
    const clickedInsideSidebar = sidebar.contains(event.target);
    const clickedOnToggleBtn = toggleBtn.contains(event.target);
    
    if (isSmallScreen && !clickedInsideSidebar && !clickedOnToggleBtn && !sidebar.classList.contains("closed")) {
      toggleSidebar();
    }
  });
  
  // Add smooth scrolling to all links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === "#") return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});