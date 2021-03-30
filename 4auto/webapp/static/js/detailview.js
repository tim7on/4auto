'use strict';
document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.querySelector('.overlay'),
        btn = document.querySelector('#connect'),
        hidden = document.querySelector('.hidden'),
        body = document.querySelector('body');

    btn.addEventListener('click', (e) => {
        e.preventDefault();
        body.style.overflow = 'hidden';
        hidden.style.display = 'flex';
        window.setTimeout(function () {
            hidden.style.opacity = 1;
        }, 0);
    });
    overlay.addEventListener('click', (e) => {
        e.preventDefault();
        const target = e.target;
        if (target && target.classList.contains('overlay')) {
            body.style.overflow = '';
            hidden.style.opacity = 0;
            window.setTimeout(function () {
                hidden.style.display = 'none';
            }, 500);
        }
    });
});