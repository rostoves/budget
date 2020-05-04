$(document).ready(function () {
    $('.comparisonBlockName').on('change', sendObjectNameUpdate);
    $('.comparisonBlockDeleteButton').on('click', objectIdToModal);
    $('#deleteObjectModalButton').on('click', deleteModalAnswer);
    $(".comparisonBlockSelect").on('change', sendComparisonObjectUpdate);
});

function sendObjectNameUpdate() {
    sendFieldUpdate('', 'update_object', this.id.slice(9), 'name', this.value);
}

function sendComparisonObjectUpdate() {
    sendFieldUpdate('', 'update_object', this.id.slice(8), 'type_id', this.value);
}

function objectIdToModal() {
    $("#deleteObjectModalButton").attr("caller-id", $(this).attr("id"));
}

function deleteModalAnswer() {
    let obj = $("#deleteObjectModalButton").attr("caller-id").slice(7);
    console.log("Category " + obj + " was deleted.");
    $("#obj_" + obj).remove();
    sendFieldUpdate('', 'delete_object_replace', obj, 'category_id', $('#newObjectSelect')[0].value);
}