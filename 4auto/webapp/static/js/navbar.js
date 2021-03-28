document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('#toggle_menu'),
        menu = document.querySelector('#menu_wrap'),
        nav_link = document.querySelectorAll('.nav_link'),
        navwrap = document.querySelector('nav');

    function hideMenu(e) {
        menu.classList.remove('show');
        // menu.classList.add('ulgrid');

    }
    btn.addEventListener('click', (e) => {
        e.preventDefault;
        target = e.target;
        menu.classList.add('show');

    });

    menu.addEventListener('mouseout', e => {
        console.log('mouse out')
        if (!menu.matches(':hover')) {
            console.log('If working')
            setTimeout(hideMenu(e), 100);
        }
    });
    document.addEventListener('touchstart', (e) => {
        if (e.target !== navwrap && !navwrap.contains(e.target)) {
            e.preventDefault;
            console.log(e.target);
            setTimeout(hideMenu(e), 100);
        }
    });
});