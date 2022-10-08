const primaryNav = document.querySelector(".navigation-item");
const navToggle = document.querySelector(".nav-toggle");

navToggle.addEventListener('click', () => {
    const visibility =  primaryNav.getAttribute('data-visible')

    if (visibility === "false")
    {
        primaryNav.setAttribute('data-visible', true);
    }
    else if (visibility === "true")
    {
        primaryNav.setAttribute("data-visible", false);
    }
})
