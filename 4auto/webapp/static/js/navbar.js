"use strict";
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('#toggle_menu'),
        menu = document.querySelector('#menu_wrap');

    btn.addEventListener('click', (e) => {
        btn.classList.toggle('opened');
        menu.className = menu.className !== 'show' ? 'show' : 'hide';
        if (menu.className === 'show') {
            setTimeout(function () {
                menu.style.display = 'block';
            }, 0); // timed to occur immediately
        }
        if (menu.className === 'hide') {
            setTimeout(function () {
                menu.style.display = 'none';
            }, 400); // timed to match animation-duration
        }
    });
});