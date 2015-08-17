
//onload functions
$(function(){
    getPrograms();
});

function getPrograms(){
    //get activities not in monthly reports for entry
    //parameters: agency_id, month, year
    var url = "/agency/wfp/get/unreportedprograms/";
    var params = {'agency_id' : $("#agency_id").val(),
		  'month'     : $("#month").val(),
		  'year'      : $("#year").val()};
    
    $.get(url, params)
	.done(function(data){
	    //data --> expects list json format
	    var options = "";
	    for(var i=0; i<data.length; i++){
		var item = data[i];
		options += "<option value='"+item.id+"'>"+item.activity+"</option>";
		item = null;
	    }
	    $("#activity").html(options);
	    console.log(data);
	});
}




function getPhysicalTargets(){
    //get physical targets of the activity
    //params : agency and year, month
    var url = "/agency/wfp/get/program/physicaltargets/";
    var month_year = new String($("#month_select").val()).split("-");
    var year = parseInt(month_year[0]);
    var month = parseInt(month_year[1]);
    var params = {"program_id" : $("#activity").val()};

    $.get(url, params)
	.done(function(data){
	    console.log(data);
	    //data is expected to be in json format
	    $("#performance_indicator").html("");
	    var content = "<table class='table table-condensed' id='accomplished_targets_table'>";
            content += "<thead>";
            content += "<tr><th>Indicator</th>";
            content += "<th>Target</th>";
            content += "<th>Accomplished</th>";
	    content += "</tr>";
            content += "</thead>";
	    content += "<tbody>";

	    for(var i=0; i<data.length; i++){
		content += "<tr id='"+data[i].id+"'>";
		content += "<td>"+data[i].indicator+"</td>";
		switch(month){
		case 1: content += "<td>" + data[i].jan + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].jan_acc+"'></td>";
		    content += "";

		    break;
		case 2: content += "<td>" + data[i].feb + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].feb_acc+"'></td>";

		    break;
		case 3: content += "<td>" + data[i].mar + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].mar_acc+"'></td>";
		    break;

		case 4: content += "<td>" + data[i].apr + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].apr_acc+"'></td>";
		    break;

		case 5: content += "<td>" + data[i].may + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].may_acc+"'></td>";
		    break;

		case 6: content += "<td>" + data[i].jun + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].jun_acc+"'></td>";
		    break;

		case 7: content += "<td>" + data[i].jul + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].jul_acc+"'></td>";
		    break;

		case 8: content += "<td>" + data[i].aug + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].aug_acc+"'></td>";
		    break;

		case 9: content += "<td>" + data[i].sept + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].sept_acc+"'></td>";
		    break;

		case 10: content += "<td>" + data[i].oct + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].oct_acc+"'></td>";
		    break;

		case 11: content += "<td>" + data[i].nov + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].nov_acc+"'></td>";
		    break;

		case 12: content += "<td>" + data[i].dec + "</td>";
		    content += "<td> <input type='number' class='form-control input-sm' id='"+data[i].id+"' value='"+data[i].dec_acc+"'></td>";
		    break;
		}
	    }
	    content += "</tbody>";
	    content += "</table>";
	    $("#performance_indicator").html(content);
	});
}


function selectRow(cur_row){
    $(cur_row).addClass("alert alert-info");
    //remove highlight to other rows
    $("table tbody tr").each(function(){
	//console.log();
	if ($(cur_row).attr("id") != $(this).attr("id")){
	    $(this).removeClass("alert alert-info");
	}
    });
}

function showAccomplishedTargets(program_id, row_obj){
    //get physical targets of the activity
    //params : agency and year, month
    var url = "/agency/wfp/get/program/physicaltargets/";
    var year = $("#id_year").val();
    var month = parseInt($("#id_month").val());
    console.log("month: " + month + " year: " + year);
    var params = {"program_id" : program_id};
    //highlight the currently selected row
    selectRow(row_obj);

    console.log("program report id: "+program_id);
    //show specific program report info
    $("#id_progrepcon div").each(function(){
	if($(this).attr("id") == ("acc_" + program_id)){
	    $(this).css("display", "block");
	}else{
	    $(this).css("display", "none");
	}
    });

    $("#acc_"+program_id).css("display", "block");
    //hide ? icon and notification
    $("#notify_block").css("display", "none");

    $.get(url, params)
	.done(function(data){
	    console.log(data);
	    //data is expected to be in json format
	    $("#performance_indicator").html("");
	    var content = "<table class='table table-condensed' id='accomplished_targets_table'>";
            content += "<thead>";
            content += "<tr><th>Indicator</th>";
            content += "<th style='text-align: right;'>Target</th>";
            content += "<th style='text-align: right;'>Accomplished</th>";
            content += "<th style='text-align: right;'>Variance</th>";
	    content += "<th></th>";
	    content += "</tr>";
            content += "</thead>";
	    content += "<tbody>";

	    for(var i=0; i<data.length; i++){
		content += "<tr id='"+data[i].id+"'>";
		content += "<td>"+data[i].indicator+"</td>";
		switch(month){
		case 1: content += "<td style='text-align: right;'>" + data[i].jan + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].jan_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].jan_acc - data[i].jan)+"</td>";
		    break;
		case 2: content += "<td style='text-align: right;'>" + data[i].feb + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].feb_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].feb_acc - data[i].feb)+"</td>";
		    break;
		case 3: content += "<td style='text-align: right;'>" + data[i].mar + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].mar_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].mar_acc - data[i].mar)+"</td>";
		    break;

		case 4: content += "<td style='text-align: right;'>" + data[i].apr + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].apr_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].apr_acc - data[i].apr)+"</td>";
		    break;

		case 5: content += "<td style='text-align: right;'>" + data[i].may + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].may_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].may_acc - data[i].may)+"</td>";
		    break;

		case 6: content += "<td style='text-align: right;'>" + data[i].jun + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].jun_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].jun_acc - data[i].jun)+"</td>";
		    break;

		case 7: content += "<td style='text-align: right;'>" + data[i].jul + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].jul_acc+"</td>";
		    content += "<td>"+(data[i].jul_acc - data[i].jul)+"</td>";
		    break;

		case 8: content += "<td style='text-align: right;'>" + data[i].aug + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].aug+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].aug_acc - data[i].aug)+"</td>";
		    break;

		case 9: content += "<td style='text-align: right;'>" + data[i].sept + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].sept_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].sept - data[i].sept_acc)+"</td>";
		    break;

		case 10: content += "<td style='text-align: right;'>" + data[i].oct + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].oct_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].oct_acc - data[i].oct)+"</td>";
		    break;

		case 11: content += "<td style='text-align: right;'>" + data[i].nov + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].nov_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].nov_acc - data[i].nov)+"</td>";
		    break;

		case 12: content += "<td style='text-align: right;'>" + data[i].dec + "</td>";
		    content += "<td style='text-align: right;'>"+data[i].dec_acc+"</td>";
		    content += "<td style='text-align: right;'>"+(data[i].dec_acc - data[i].dec)+"</td>";
		    break;
		}
	    }
	    content += "</tbody>";
	    content += "</table>";
	    $("#performance_table").html(content);
	});
}

function savePerformanceReport(){
    var performances = [];
    $("#accomplished_targets_table > tbody tr").each(function(){
	var id = $(this).attr("id");

	performances.push(
	    {"id"   : id,
	     "acc"  : $(this).find("input").val()}
	);
    });

    var month_year = new String($("#month_select").val()).split("-");

    var params = {"activity_id"    : $("#activity").val(),
		  "received"       : $("#received").val(),
		  "incurred"       : $("#incurred").val(),
		  "performances"   : performances ,
		  "year"           : parseInt(month_year[0]),
		  "month"          : parseInt(month_year[1]),
		  "remarks"        : $("#remarks_id").val()
		 }

    console.log(params);

    $.ajax({contentType: "application/json",
    	    dataType : "json",
    	    type: "POST",
    	    processData : false,
    	    url  : "/agency/add_performance_report",
    	    data : JSON.stringify(params)
    	   })
    	.done(function(data){
    	    console.log(data);
    	    window.location = "/agency/monthly_reports?year=" + params.year + "&month=" + params.month;
    	})
    	.fail(function(data){
    	    console.log(data.responseText);
    	});
}


function deleteReport(report_id){
    var params = {"id": report_id};
    var conf = confirm('Are you sure to delete this report?');
    if (conf==1){
	$.ajax({contentType: "application/json",
		dataType    : "json",
		type        : "POST",
		processData : false,
		url         : "/agency/remove_report",
		data        : JSON.stringify(params)
	       })
	    .done(function(data){
		console.log(data)
		if (data.status == "success"){
		    window.location = "/agency/monthly_reports?year="+data.year+"&month="+data.month;
		}
	    })
	    .fail(function(data){
		console.log(data.responseText)
	    });

    }
}


$("#id_year").change(function(){
    $("#monthly_report_search_form").submit();
});

$("#id_month").change(function(){
    $("#monthly_report_search_form").submit();
});


