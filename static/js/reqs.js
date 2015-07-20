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
    var quarter = $("#id_quarter").val();
    var agency_id = $("#agency_id").val();
    var year = $("#year").val();

    var data = {'quarter': quarter,
		'year'   : year,
		'agency_id' : agency_id
	       }

    $.get("/main/display_sub_qreqs", data, function(rs){
	$("#sqreqs").html(rs);
    });
}


function removeQReq(id){
    var data = {id: id};
    $.ajax({
	url  : "/requirements/delete_quarter_sub_req",
	data : data,
	type : "GET",
	success: function(data){
	    showSubmittedQReqs();
	},
	error: function(xhr, textStatus, errorThrown){
	    alert(textStatus + ": " + errorThrown);
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

function setQuarterSubmitReq(self, action){
    quarter = $("#id_quarter").val();
    req_id  = self.value;
    agency_id = $("#id_agency_id").val();

    if (self.checked){
	//set values to fields
	$("#md_req_action").val(action);
	$("#md_quarter").val(quarter);
	$("#md_req_id").val(req_id);
	$("#md_agency_id").val(agency_id);
	$("#id_reqsDateInputForm").modal("show");
    }

}


function setEditDateQRS(qrs_id, date_submit){
    //qrs_id : submitted quarter requirement idx
    //date_submit : current submitted date of the requirement
    $("#md_qrs_id").val(qrs_id);
    $("#md_date").val(date_submit);
    $("#md_req_action").val("edit");
    $("#md_agency_id").val($("#id_agency_id").val());
    $("#id_reqsDateInputForm").modal("show");
}

//close date input modal for quarterly requirements
$("#close_activity_modal").click(function(){
    req_id = $("#md_req_id").val();
    $("#qchk-"+req_id).attr("checked", false);
});


$(".close").click(function(){
    req_id = $("#md_req_id").val();
    $("#qchk-"+req_id).attr("checked", false);

});



function submitQuarterReq(){
    var data = {'req_id'  : $("#md_req_id").val(),
		'quarter' : $("#md_quarter").val(),
		'action'  : $("#md_req_action").val(),
		'agency_id' : $("#md_agency_id").val(),
		'date_submit' : $("#md_date").val(),
		'year'     : $("#md_year").val(),
		'qrs_id'   : $("#md_qrs_id").val()
	       };

    $.ajax({
	url  : "/main/submit_quarter_reqs",
	data : data,
	type : "GET",
	success: function(json){
	    //console.log(json[0].id);
	    $("#id_reqsDateInputForm").modal("hide");
	    showSubmittedQReqs();
	},
	error: function(xhr, textStatus, errorThrown){
	    alert(textStatus + ": " + errorThrown);
	}
    });
    //show submitted requirements

    
}
