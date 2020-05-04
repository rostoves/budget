$(document).ready(function () {
    prepareButtons();
});

function prepareButtons() {
    $('.comparisonBlockName').on('change', sendObjectNameUpdate);
    $('.comparisonBlockDeleteButton').on('click', objectIdToModal);
    $('#deleteObjectModalButton').on('click', deleteModalAnswer);
    $(".comparisonBlockSelect").on('change', sendComparisonObjectUpdate);
    $('#objectsSearchInput').on('change', sendFilter);
    $('.paginationPage').on('click', sendFilter);
}

function sendObjectNameUpdate() {
    sendFieldUpdate('', 'update_object', this.id.slice(9), 'name', this.value);
}

function sendComparisonObjectUpdate() {
    sendFieldUpdate('', 'update_object', this.id.slice(8), 'merchant_code_id', this.value);
}

function objectIdToModal() {
    $("#deleteObjectModalButton").attr("caller-id", $(this).attr("id"));
}

function deleteModalAnswer() {
    let obj = $("#deleteObjectModalButton").attr("caller-id").slice(7);
    console.log("Description " + obj + " was deleted.");
    $("#obj_" + obj).remove();
    sendFieldUpdate('', 'delete_object_replace', obj, 'description_id', $('#newObjectSelect')[0].value);
}

function sendFilter() {
    let page_number  = findPageNumber(this);
    let search_name = $('#objectsSearchInput')[0].value;

    $.ajax({
        url: "",
        type: "GET",
        dataType: "json",
        data: {
            filter_applied: 'True',
            page: page_number,
            name: search_name
        },
        complete: function (data) {
            $('.objectListContainer').html(data.responseText);
            prepareButtons();
        }
    });
}

function findPageNumber(object) {
    let currentPage = $('.currentPaginationPage').length > 0 ? $('.currentPaginationPage').attr('id').slice(5) : '1';
    return object.classList.contains('paginationPage') ? object.id.slice(5) : currentPage;
}