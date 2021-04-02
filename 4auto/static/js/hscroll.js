'use strict';
document.addEventListener('DOMContentLoaded', () => {
  const area = document.querySelector('.scroll_horizontal');

  area.addEventListener('wheel', function (e) {
    if (e.type != 'wheel') {
      return;
    }
    let delta = ((e.deltaY || -e.wheelDelta || e.detail) >> 10) || 1;
    delta = delta * (-250);
    area.scrollLeft -= delta;
    e.preventDefault();

  });
});