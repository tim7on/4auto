document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('#toggle_menu'),
        menu = document.querySelector('#menu_wrap'),
        nav_link = document.querySelectorAll('.nav_link'),
        navwrap = document.querySelector('nav');

    function hideMenu(e) {
        e.preventDefault;
        menu.className = menu.className !== 'show' ? 'show' : 'hide';
        setTimeout(function () {
            menu.style.display = 'none';
        }, 500);

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
            }, 500); // timed to match animation-duration
        }
    });
    menu.addEventListener('mouseout', e => {
        console.log('mouse out')
        if (!menu.matches(':hover')) {
            hideMenu(e);
        }
    });
    document.addEventListener('touchend', (e) => {
        if (menu.className === 'show') {
            if (e.target !== navwrap && !navwrap.contains(e.target)) {
                hideMenu(e);
            }
        }
    });
});