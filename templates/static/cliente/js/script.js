document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector("header");

    window.addEventListener("scroll", function() {
        header.classList.toggle("sticky", window.scrollY > 0);
    });

    let menu = document.querySelector('#menu-icon');
    let navlist = document.querySelector('.navlist');

    if (menu) {
        menu.onclick = () => {
            menu.classList.toggle('bx-x');
            if (navlist) {
                navlist.classList.toggle('open');
            }
        };
    }

    window.onscroll = () => {
        if (menu) {
            menu.classList.remove('bx-x');
        }
        if (navlist) {
            navlist.classList.remove('open');
        }
    };

    const sr = ScrollReveal({
        distance: '30px',
        duration: 2600,
        reset: true
    });

    // sr.reveal('.home-text', { delay: 280, origin: 'bottom' });
    // sr.reveal('.featured, .cta, .new, .brand, .contact', { delay: 200, origin: 'bottom' });

    // Esconde as mensagens de sucesso após 5 segundos
    setTimeout(function() {
        var messages = document.querySelectorAll('.alert');
        messages.forEach(function(message) {
            message.style.display = 'none';
        });
    }, 5000); // 5000 milissegundos = 5 segundos
});

