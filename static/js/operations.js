$(document).ready(function () {
    $('.operationListFilter').on('change', sendFilter);
});

function sendFilter() {
    let status = collectSelectedValues('status');
    let merchant_code = collectSelectedValues('merchant_code');

    $.ajax({
        url: "",
        type: "GET",
        dataType: "json",
        data: {
            filter_applied: 'True',
            status: status,
            merchant_code: merchant_code
        },
        complete: function (data) {
            $('.operationsListTableContainer').html(data.responseText);
        }
    });
}

function collectSelectedValues(filter) {
    let arr = [];
    $('#filter_'+filter+' option:selected').each(function() {
        arr.push(this.value);
    });

    return arr;
}