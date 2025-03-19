document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebarToggleBtn");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("active");
        });
    }
});

function confirmDelete(postId) {
    Swal.fire({
        title: "Are you sure?",
        text: "This action cannot be undone!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/blog/del_post/${postId}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token() }}"  // If using Flask-WTF CSRF protection
                }
            }).then(response => {
                if (response.ok) {
                    Swal.fire("Deleted!", "Your post has been deleted.", "success")
                        .then(() => location.reload());
                } else {
                    Swal.fire("Error!", "Failed to delete post.", "error");
                }
            });
        }
    });
}
