$(document).ready(function () {
    $('.calculatorFormInput').on('change', calcBalance);
});

function calcBalance() {
    var deposit = parseFloat($('#deposit')[0].value);
    var debit = parseFloat($('#debit')[0].value);
    var credit = -390000+parseFloat($('#credit')[0].value);
    var savings = parseFloat($('#savings')[0].value);
    var bi_result = parseFloat($('#bi_result')[0].value);

    console.log(deposit,debit,credit,savings,bi_result);

    let total = deposit + debit + credit + savings;
    total = Math.round(total.toFixed(3) * 100) / 100;
    let diff = total - bi_result;
    diff = Math.round(diff.toFixed(3) * 100) / 100;

    $("#total").text(total);
    $("#diff").text(diff);
}