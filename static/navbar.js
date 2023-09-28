const mobileDropdown = document.getElementById("mobille");
const mobileNav = document.querySelectorAll("#header .mobile li");
const mobile = document.querySelector(".mobile")
const mobilea= document.querySelector("#kapat")

let i = 1;

mobileDropdown.addEventListener("click", function () {
    if (i === 1) {
        mobile.style.display = "block";
        mobileNav.forEach(function (li) {
            li.style.display = "block";
            li.style.height="50px";
        });
        mobilea.innerHTML="X";
        // Sayfa üzerindeki herhangi bir yere tıklandığında çağrılacak işlev
    } else if (i === 2) {
        mobile.style.display = "none";
        mobileNav.forEach(function (li) {
            li.style.display = "none";
            i=0;
        mobilea.innerHTML="Menu";

        });
    }
    i += 1;
});
