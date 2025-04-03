document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("sidebarToggle");
  const mainContent = document.getElementById("main");


  // Adjust layout responsively on window resize
  window.addEventListener("resize", () => {
    if (window.innerWidth <= 768) {
      // For small screens, hide sidebar and set toggle button to the left
      sidebar.classList.add("closed");
      toggleBtn.style.left = "20px";
      mainContent.style.marginLeft = "0";
    } else {
      // For larger screens, show sidebar and reset margins
      sidebar.classList.remove("closed");
      toggleBtn.style.left = "260px";
      mainContent.style.marginLeft = "250px";
    }
  });

  // Trigger the resize event once to set the initial layout correctly
  window.dispatchEvent(new Event("resize"));
});
