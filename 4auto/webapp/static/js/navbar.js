document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('#toggle_menu'),
        menu = document.querySelector('#menu_wrap'),
        menu_ul = document.querySelector('.menu_ul'),
        nav_link = document.querySelectorAll('.nav_link'),
        navwrap = document.querySelector('nav');

    function hideMenu(e) {
        e.preventDefault;
        menu.className = menu.className !== 'show' ? 'show' : 'hide';
        setTimeout(function () {
            menu.style.display = 'none';
        }, 250);

    }
    btn.addEventListener('click', (e) => {
        menu.className = menu.className !== 'show' ? 'show' : 'hide';
        if (menu.className === 'show') {
            setTimeout(function () {
                menu.style.display = 'block';
            }, 0); // timed to occur immediately
        }
        if (menu.className === 'hide') {
            setTimeout(function () {
                menu.style.display = 'none';
            }, 250); // timed to match animation-duration
        }
    });

    // MOUSE LEAVE FOR ANOTHER OBJECTS???
    // 
    // menu_ul.addEventListener('mouseleave', e => {
    //     console.log(e.currentTarget);
    //     if (!menu.contains(e.currentTarget) || !menu.matches(':hover') || menu.matches(':after')) {
    //         console.log('IF WORKED');
    //         hideMenu(e);
    //     }
    // });

    document.addEventListener('touchstart', (e) => {
        if (menu.className === 'show') {
            if (e.target !== navwrap && !navwrap.contains(e.target)) {
                hideMenu(e);
            }
        }
    });
    document.addEventListener('click', (e) => {
        if (menu.className === 'show') {
            if (e.target !== navwrap && !navwrap.contains(e.target)) {
                hideMenu(e);
            }
        }
    });
});