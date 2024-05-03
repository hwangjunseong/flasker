const categoryTitleLinks = document.querySelectorAll(".categoryTitleLink");

categoryTitleLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent the default link behavior

    // Get the title value from the clicked link's data attribute
    const title = link.getAttribute("data-title");

    // Set the title value to the form input field
    document.getElementById("categoryTitle").value = title;
  });
});
