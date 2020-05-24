let mccArray = [];

$(document).ready(function () {
    $('.importMcc').on('change', markNewMcc);
    $('.splitImportRowButton').on('click', rowInsertAfter);
    $('.deleteImportRowButton').on('click', rowDelete);
    $('.importTableButton').on('click', collectImportArray);
    loadData('', 'get_mcc', function () {
        mccArray = this;
        console.log(mccArray);
        autocompleteMcc();
        $('.importMcc').each(markNewMcc);
    });
});


function markNewMcc() {
    let _mcc = this.value;
    let _id = '#'+this.id;

    if (mccArray.indexOf(_mcc) === -1 ) {
        // console.log('Marked new mcc ' + _id);
        $(_id).addClass("badge-info");
    } else {
        // console.log('Cleaned old mcc ' + _id);
        $(_id).removeClass("badge-info");
    }
}

function autocompleteMcc() {
    $('.importMcc').autocomplete({
        source: mccArray
    });
}

function rowInsertAfter() {
    let row = this.id.slice(6);
    let id = getRandom();
    let date = "<input class='date' type='text' id='date_" + id + "' value='" + $('#date_'+row)[0].value + "'>";
    let acc = "<span class='account' id='acc_" + id + "'>" + $('#acc_'+row)[0].innerText + "</span>";
    let status = "<span class='status' id='status_" + id + "'>" + $('#status_'+row)[0].innerText + "</span>";
    let op_sum = "<input class='operation_sum' id='op_sum_" + id + "' value='0.00'>";
    let op_cur = "<span class='operation_cur' id='op_cur_" + id + "'>" + $('#op_cur_'+row)[0].innerText + "</span>";
    let bar_sum = "<input class='bargain_sum' id='bar_sum_" + id + "' value='0.00'>";
    let bar_cur = "<span class='bargain_cur' id='bar_cur_" + id + "'>" + $('#bar_cur_'+row)[0].innerText + "</span>";
    let mcc = "<input class='merchant_code importMcc' type='text' id='mcc_" + id + "' value='" + $('#mcc_'+row)[0].value + "'>";
    let mcc_orig = "<input class='merchant_code_original' type='hidden' id='mcc_orig_" + id + "' value='" + $('#mcc_orig_'+row)[0].value + "'>";
    let desc = "<input class='description' id='desc_" + id + "' value='" + $('#desc_'+row)[0].value + "'>";
    let comment = "<input class='comment' type='text' placeholder='Комментарий'>";
    let deleteImportRowButton = "<button class='deleteImportRowButton' id='delete_" + id + "'>Удалить</button>";
    $( $( "#row_" + row) ).after(
        "<div class='importTableRow' id='row_" + id + "'>"
        + date + acc + status + op_sum + op_cur + bar_sum + bar_cur + mcc + mcc_orig + desc + comment + deleteImportRowButton +
        "</div>"
    );
    autocompleteMcc();
    $('#mcc_'+ id).on('click', markNewMcc);
    $('.deleteImportRowButton').on('click', rowDelete);
}

function rowDelete() {
    let row = this.id.slice(7);
    console.log("#row_" + row + " was deleted.");
    $("#row_" + row).remove();
}

function collectImportArray() {
    importTableArray = [];
    $(".importTableRow").each(function() {
        let arrayOfThisRow = {};
        let tableData = $(this).children();
        for (let i = 0; i < tableData.length; i++) {
            switch (tableData[i].nodeName) {
                case "INPUT":
                    arrayOfThisRow[tableData[i].classList[0]] = tableData[i].value;
                    break;
                case "SPAN":
                    arrayOfThisRow[tableData[i].classList[0]] = tableData[i].innerText;
                    break;
            }
        }
        arrayOfThisRow['id'] = this.id;

        importTableArray.push(arrayOfThisRow);
    });

    // console.log(importTableArray);

    sendPOST('', 'import_table', importTableArray, function () {
        renderResultsTable(this);
        // this['not_inserted'].length > 0 ? renderResultsTable(this) : loadOplistWithOutdatedPlans();
    });
}

function renderResultsTable(arr) {
    arr.inserted.forEach(function(item, i, arr) {
        $("#"+item).remove();
    });
    if (arr.not_inserted.length < 1) {
            console.log('ok');
    } else {
        arr.not_inserted.forEach(function (item, i, arr) {
            $("#" + item).addClass("badge-warning");
        });
    }
}

// function loadOplistWithOutdatedPlans() {
//     // window.open("/operations/?filter_applied=True&page=1&status%5B%5D=PLAN&date_to="+getToday(), "_self");
//
// }