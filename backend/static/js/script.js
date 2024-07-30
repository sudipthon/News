// Mobile

const hamburgericon = document.querySelector("#mbl-menu-icon");
const closebtn = document.querySelector(".close-btn");
const mblmenuitems = document.querySelector(".header-main-menu");
const midbar = document.querySelector(".midbar");


// Hamburger Click Event
hamburgericon.addEventListener("click", () => {
  if (screen.width < 768) {
    mblmenuitems.classList.toggle("mblopen");
  }
});

// Close Button Event
closebtn.addEventListener("click", () => {
    mblmenuitems.classList.remove("mblopen");
});

// Mobile Menu Remove
window.addEventListener("resize", ()=>{
  if (window.innerWidth > 768 ) {
    mblmenuitems.classList.remove("mblopen");
}
});

// Sticky Header
window.addEventListener("scroll", ()=>{
  if(window.scrollY > 170){
    document.querySelector(".menu-bar").classList.add("sticky")
  }else{
    document.querySelector(".menu-bar").classList.remove("sticky")
  }
})

// Sticky Mobile Menu Bar
window.addEventListener("scroll", ()=>{
  if(window.scrollY > 45){
    document.querySelector(".midbar").classList.add("sticky")
  }else{
    document.querySelector(".midbar").classList.remove("sticky")
  }
})

// Swiper

const swiper = new Swiper('.swiper', {
  slidesPerView: 2,
  spaceBetween: 15,
  // Optional parameters
  loop: true,

  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
  },

  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },

  breakpoints: {
    768: {
      slidesPerView: 3,
      spaceBetween: 40,
    },
    1024: {
      slidesPerView: 4,
      spaceBetween: 10,
    },
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  // And if we need scrollbar
  scrollbar: {
    el: '.swiper-scrollbar',
  },
});


// Pop Up

document.addEventListener('DOMContentLoaded', () => {

  let popup = document.getElementById("pop-up");

  if (popup && window.location.pathname === '/') {

      let closePopup = document.getElementById("popup-close");



      // Check if the popup has been shown before

      if (!sessionStorage.getItem('popupShown')) {

          // Show the popup if it hasn't been shown before

          setTimeout(() => {

              popup.classList.remove("d-none");

          }, 1000);

          sessionStorage.setItem('popupShown', true);

          document.body.style.overflow = "hidden";

      }



      // Add event listener to close the popup and clear sessionStorage

      closePopup.addEventListener("click", () => {

          popup.classList.add("d-none");

          document.body.style.overflow = "auto";

          sessionStorage.setItem('popupShown', true);

      });

  }

});
