'use strict';
document.addEventListener('DOMContentLoaded', () => {

	const scroll = document.querySelectorAll('.scroll_horizontal');

	scroll.forEach(area => {
		area.addEventListener('wheel', function (e) {
			let delta = ((e.deltaY || -e.wheelDelta || e.detail) >> 10) || 1;
			delta = delta * (-250);
			area.scrollLeft -= delta;
		});
	});

});