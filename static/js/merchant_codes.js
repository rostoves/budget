$(document).ready(function () {
    $('.comparisonBlockName').on('change', sendObjectNameUpdate);
    $('.comparisonBlockDeleteButton').on('click', objectIdToModal);
    $('#deleteObjectModalButton').on('click', deleteModalAnswer);
    $(".comparisonBlockSelect").on('change', sendComparisonObjectUpdate);
    $(".activeBlockSelect").on('change', sendActiveObjectUpdate);
});

function sendObjectNameUpdate() {
    sendFieldUpdate('', 'update_object', this.id.slice(9), 'name', this.value);
}

function sendComparisonObjectUpdate() {
    sendFieldUpdate('', 'update_object', this.id.slice(8), 'category_id', this.value);
}

function sendActiveObjectUpdate() {
    console.log(this)
    sendFieldUpdate('', 'update_object', this.id.slice(8), 'active', this.value);
}

function objectIdToModal() {
    $("#deleteObjectModalButton").attr("caller-id", $(this).attr("id"));
}

function deleteModalAnswer() {
    let obj = $("#deleteObjectModalButton").attr("caller-id").slice(7);
    console.log("Merchant Code " + obj + " was deleted.");
    $("#obj_" + obj).remove();
    sendFieldUpdate('', 'delete_object_replace', obj, 'merchant_code_id', $('#newObjectSelect')[0].value);
}