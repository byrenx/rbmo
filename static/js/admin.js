function setContentTLetter(){
    var reg_treas = $('#reg_treasurer').val();
    var fiscal = $('#fiscal').val();
    var content = $('#content').val();
    var oic = $('#oic').val();

    $('#reg_tresurer_name').html(reg_treas);
    $('#fiscal_name').html(fiscal);
    $('#letter_content').html(content);
    $('#letter_oic').html(oic);
}
