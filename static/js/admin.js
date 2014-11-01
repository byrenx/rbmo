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


function printSCMA(allocation){
    var approval = "";
    var approved = "";
    var html = "";
    if (allocation=="PS"){
	approval = $("#approval_name").val();
	html = "APPROVED:</br></br><b>"+approval+"</b></br>Executive Director, RBMO";
	$("#approval_pane").html(html);
	$("#scma_print").printArea();
    }else if( allocation=="MOOE"){
	approval = $("#approval_name").val();
	approved = $("#approved_name").val();
	var html_left = "RECOMMENDING APPROVAL:</br></br><b>"+approval+"</b></br>Executive Director, RBMO";
	$("#approval_pane").html(html_left);
	var html_right = "APPROVED:</br></br><b>"+approved+"</b></br>Regional Governor, ARMM";
	$("#approved_pane").html(html_right);
	$("#scma_print").printArea();
    }else{
	
    }
}
