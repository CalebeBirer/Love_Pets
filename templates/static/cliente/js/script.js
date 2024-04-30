const header = document.querySelector("header");

window.addEventListener("scroll", function() {
    header.classList.toggle("sticky", window.scrollY > 0);
});

let menu = document.querySelector('#menu-icon');
let navlist = document.querySelector('.navlist');
let contact = document.querySelector('.contact');   


menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navlist.classList.toggle('open');
};

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navlist.classList.remove('open');
}

const sr = ScrollReveal ({
    distance: '30px',
    duration: 2600,
    reset: true
})

//sr.seveal('.home-text',{delay:280, origin:'botton'})

//sr.seveal('.featured,.cta,.new,.brand,.contact',{delay:200, origin:'botton'})