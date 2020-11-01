$(document).ready(function () {
    prepareButtons();
});

function prepareButtons() {
    $('.operationListFilter').on('change', sendFilter);
    $('.paginationPage').on('click', sendFilter);
    $('.deleteOperationButton').on('click', objectIdToModal);
    $('#deleteObjectModalButton').on('click', deleteModalAnswer);
    $('#addOperationModalButton').on('click', addOperation);
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

function addOperation() {
    console.log('Adding operation.');
    let status = $('#addOperationStatus')[0].value;
    let date = new Date($('#addOperationDate')[0].value);
    let account = $('#addOperationAccount')[0].value;
    let sum = $('#addOperationSum')[0].value;
    let mcc = $('#addOperationMcc')[0].value;
    let desc = $('#addOperationDesc')[0].value;
    let comment = $('#addOperationComment')[0].value;
    let operation = [{
            'id': 1,
            'manual_insert': 1,
            'date': date,
            'account': account,
            'status': status,
            'operation_sum': sum,
            'operation_cur': 'RUB',
            'bargain_sum': sum,
            'bargain_cur': 'RUB',
            'merchant_code': mcc,
            'description': desc,
            'comment': comment
        }];


    if ($('#addOperationDateRepeat').prop("checked")) {
        console.log('Repeatable operation, every ' + $('#addOperationDatePeriod')[0].value);
        for (let i = 1; i < $('#addOperationRepeatCount')[0].value; i++) {
            operation.push({
                'id': i + 1,
                'manual_insert': true,
                'date': calculateRepeatDate(date, i, $('#addOperationDatePeriod')[0].value),
                'account': account,
                'status': status,
                'operation_sum': sum,
                'operation_cur': 'RUB',
                'bargain_sum': sum,
                'bargain_cur': 'RUB',
                'merchant_code': mcc,
                'description': desc,
                'comment': comment
            });
        }
    }

    console.log(operation);
    sendPOST('', 'add_operation', operation, function () {
        console.log(this);
    });
}

function calculateRepeatDate(_date, _count, _period) {
    let function_date = new Date(_date);

    switch (_period) {
        case 'month':
            function_date.setMonth(function_date.getMonth() + _count);
            break;
        case 'week':
            function_date.setDate(function_date.getDate()+7*_count);
            break;
        case 'day':
            function_date.setDate(function_date.getDate() + _count);
            break;
        case 'year':
            function_date.setFullYear(function_date.getFullYear() + _count);
            break;
    }
    return function_date;
}