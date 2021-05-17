"use strict";
let deleteBtn = document.querySelectorAll('.delete'),
    upBtn = document.querySelectorAll('.up');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function deletePost(item) {
    let action = confirm('Вы действительно хотите удалить пост?'),
        slug = item.getAttribute('data-slug'),
        pk = item.getAttribute('data-id'),
        card = document.querySelector('#item_' + pk),
        url = slug + 'delete/';
    console.log(slug);
    console.log(url);

    if (action != false) {
        $.ajax({
            method: 'POST',
            url: url,
            dataType: 'json',
            success: function (data) {
                card.remove();
            }
        });
    }
}

function upPost(item) {
    let slug = item.getAttribute('data-slug'),
        url = slug + 'up/';
    $.ajax({
        method: 'POST',
        url: url,
        dataType: 'json',
        success: function () {
            location.reload();
        }
    });

}
upBtn.forEach(element => {
    element.addEventListener('click', e => {
        upPost(e.target);
    });
});
deleteBtn.forEach(element => {
    element.addEventListener('click', e => {
        deletePost(e.target);
    });

});