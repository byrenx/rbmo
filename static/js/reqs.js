function removeReqMode(tag_id, req_sub_id){
    $('#'+tag_id+' span').removeClass().addClass('glyphicon glyphicon-remove text-danger');
}

function viewReqStatmode(tag_id){
    $('#'+tag_id+' span').removeClass().addClass('glyphicon glyphicon-check text-success');
}


function removeMonthlyReqMode(tag_id, req_sub_id){
    $('#'+tag_id+' span').removeClass().addClass('glyphicon glyphicon-remove text-danger');
}


function showSubmittedQReqs(){
    var quarter = $("#quarter").val();
    var agency_id = $("#agency_id").val();
    var year = $("#year").val();

    var data = {'quarter': quarter,
		'year'   : year,
		'agency_id' : agency_id
	       }

    $.get("/admin/display_sub_qreqs", data, function(rs){
	$("#sqreqs").html(rs);
    });
}
