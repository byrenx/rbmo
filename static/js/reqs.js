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


function removeQReq(id, requirement_id, quarter){
    var data = {id: id}
    $.get("/requirements/delete_quarter_sub_req", data, function(rs){
	rs = new String(rs).trim();
	if (rs=="done"){
	    //delete_row
	    $("#qreq"+id).remove();
	    removeQReqStatus(quarter, requirement_id)
	}
    });
}

function removeQReqStatus(quarter, requirement_id){
    var html =  "<input type='checkbox' name='qr[]' value='"+quarter+";"+requirement_id+"'/>";
    if(quarter==1){
	$("#q1"+requirement_id).html(html);
    }else if(quarter==2){
	$("#q2"+requirement_id).html(html);
    }else if(quarter==3){
	$("#q3"+requirement_id).html(html);
    }else{
	$("#q4"+requirement_id).html(html);
    }
}

function setQuarterSubmitReq(self){
    q_rid = self.value.split(';');
    quarter = q_rid[0]
    req_id  = q_rid[1]
    agency_id = $("#id_agency_id").val();

    if (self.checked){
	//set values to fields
	$("#md_req_action").val("add");
	$("#md_quarter").val(quarter);
	$("#md_req_id").val(req_id);
	$("#md_agency_id").val(agency_id);
	$("#id_reqsDateInputForm").modal("show");
    }

}



function submitQuarterReq(){
    var data = {'req_id'  : $("#md_req_id").val(),
		'quarter' : $("#md_quarter").val(),
		'action'  : $("#md_req_action").val(),
		'agency_id' : $("#md_agency_id").val(),
		'date_submit' : $("#md_date").val(),
		'year'     : $("#md_year").val()
	       };

    $.ajax({
	url  : "/admin/submit_quarter_reqs",
	data : data,
	type : "GET",
	dataType: "json",
	success: function(json){
	    console.log(json[0].id)
	},
	error: function(xhr, textStatus, errorThrown){
	    alert(textStatus + ": " + errorThrown);
	}
    });
    
}
