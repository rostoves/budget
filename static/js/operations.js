$(document).ready(function () {
    prepareButtons();
});

function prepareButtons() {
    $('.operationListFilter').on('change', sendFilter);
    $('.paginationPage').on('click', sendFilter);
    $('.deleteOperationButton').on('click', objectIdToModal);
    $('#deleteObjectModalButton').on('click', deleteModalAnswer);
    $('.operationListDate').on('change', sendOperationDateUpdate);
    $('.operationListComment').on('change', sendOperationCommentUpdate);
    $('.operationListSum').on('change', sendOperationSumUpdate);
    $('.operationListMccSelect').on('change', sendOperationMccUpdate);
}

function sendOperationDateUpdate() {
    sendFieldUpdate('', 'update_operation', this.id.slice(5), 'date', this.value);
}

function sendOperationCommentUpdate() {
    sendFieldUpdate('', 'update_operation', this.id.slice(8), 'comment', this.value);
}

function sendOperationSumUpdate() {
    sendFieldUpdate('', 'update_operation', this.id.slice(4), 'bargain_sum', this.value);
}

function sendOperationMccUpdate() {
    sendFieldUpdate('', 'update_operation', this.id.slice(11), 'merchant_code_id', this.value);
}

function objectIdToModal() {
    $("#deleteObjectModalButton").attr("caller-id", $(this).attr("id"));
}

function deleteModalAnswer() {
    let obj = $("#deleteObjectModalButton").attr("caller-id").slice(7);
    console.log("Operation " + obj + " was deleted.");
    $("#row_" + obj).remove();
    sendPOST('', 'delete_operation', obj);
}

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
            prepareButtons();
        }
    });
}

function findPageNumber(object) {
    let currentPage = $('.currentPaginationPage').length > 0 ? $('.currentPaginationPage').attr('id').slice(5) : '1';
    return object.classList.contains('paginationPage') ? object.id.slice(5) : currentPage;
}