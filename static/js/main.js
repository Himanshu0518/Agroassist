document.addEventListener("DOMContentLoaded", function () {
  let sidebar = document.getElementById("sidebar");
  let toggleBtn = document.getElementById("sidebarToggle");
  let mainContent = document.getElementById("main");

  // Toggle sidebar visibility
  toggleBtn.addEventListener("click", function () {
      // Toggle the sidebar's closed class
      sidebar.classList.toggle("closed");

      // If sidebar is closed, remove main content margin; else, add margin equal to sidebar width
      if (sidebar.classList.contains("closed")) {
          toggleBtn.style.left = "20px"; // Move toggle button to the left
          mainContent.style.marginLeft = "0"; // Remove extra space
      } else {
          toggleBtn.style.left = "260px"; // Position toggle button aligned with sidebar
          mainContent.style.marginLeft = "250px"; // Reserve space for sidebar
      }
  });

  // Responsive behavior on window resize
  window.addEventListener("resize", () => {
      if (window.innerWidth <= 768) {
          // For small screens, always hide sidebar and remove margin
          sidebar.classList.add("closed");
          toggleBtn.style.left = "20px";
          mainContent.style.marginLeft = "0";
      } else {
          // For larger screens, show sidebar and set margin
          sidebar.classList.remove("closed");
          toggleBtn.style.left = "260px";
          mainContent.style.marginLeft = "250px";
      }
  });

  // Trigger resizing once to set initial layout
  window.dispatchEvent(new Event("resize"));
});
