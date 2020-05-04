var csrftoken = getCookie('csrftoken');

function loadData(_url, _action, callback) {
    console.log(_url, _action);
    $.ajax({
        url: _url,
        type: "POST",
        dataType: "json",
        headers: {'X-CSRFToken': csrftoken},
        data: {
            action: _action
        },
        success: function (data) {
            callback.call(data);
        }
    });
}

function sendPOST(_url, _action, _data = undefined, callback = undefined) {
    console.log(_url, _action, _data);
    $.ajax({
        url: _url,
        type: "POST",
        dataType: "json",
        headers: {'X-CSRFToken': csrftoken},
        data: {
            action: _action,
            data: JSON.stringify(_data)
        },
        success: function (data) {
            console.log(data);
            callback.call(data);
        }
    });
}

function sendFieldUpdate(_url, _action, _rowId, _field, _newValue) {
    console.log(_action, _rowId, _field, _newValue);
    $.ajax({
        url: _url,
        type: "POST",
        dataType: "json",
        headers: {'X-CSRFToken': csrftoken},
        data: {
            action: _action,
            id: _rowId,
            field: _field,
            new_value: _newValue
        },
        success: function (data) {}
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getRandom() {
    return Math.floor(Math.random() * (1000000 - 100000 + 1)) + 100000;
}