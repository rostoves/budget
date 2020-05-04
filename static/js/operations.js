$(document).ready(function () {
    $('.operationListFilter').on('change', sendFilter);
    $('.operationListPage').on('click', sendFilter);
});

function sendFilter() {
    let status = $('#filter_status').val();
    let merchant_code = $('#filter_merchant_code').val();
    let category = $('#filter_category').val();
    let type = $('#filter_type').val();
    let date_from = $('#filter_date_from')[0].value;
    let date_to = $('#filter_date_to')[0].value;
    let page_number  = findPageNumber(this);
    let orderby = $('#filter_orderby')[0].value;

    $.ajax({
        url: "",
        type: "GET",
        dataType: "json",
        data: {
            filter_applied: 'True',
            status: status,
            date_from: date_from,
            date_to: date_to,
            merchant_code: merchant_code,
            category: category,
            type: type,
            page: page_number,
            orderby: orderby
        },
        complete: function (data) {
            $('.operationsListTableContainer').html(data.responseText);
            $('.operationListPage').on('click', sendFilter);
        }
    });
}

function findPageNumber(object) {
    let currentPage = $('.currentListPage').length > 0 ? $('.currentListPage').attr('id').slice(5) : '1';
    return object.classList.contains('operationListPage') ? object.id.slice(5) : currentPage;
}