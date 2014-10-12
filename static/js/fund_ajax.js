function getAllocBudget(){
    $.get('/agency/fund/get_budget',
	  {'agency_id' : $('#agency_id').val(),
	   'month'     : $('#id_month').val(),
	   'year'      : $('#id_year').val(),
	   'allocation': $('#id_allocation').val()
	  },
	  function(data){
	      var amount_bal = JSON.parse(data)
	      $('#budget').html(amount_bal.amount);
	      $('#balance').html(amount_bal.balance);
	      $('#id_amount').val(amount_bal.balance);
	      $("#note").removeClass().html("");

	      
	      if(amount_bal.balance<=0 && amount_bal.amount<=0){
		  $("#note").addClass("alert alert-danger").
		      html("No budget allocated for this month, Releasing of fund is not permitted");
		  $("#id_submit").attr("disabled", "disabled");
	      }else if(amount_bal.balance<=0 && amount_bal.amount>0){
		  $("#note").addClass("alert alert-danger").
		      html("<span class='glyphicon glyphicon-warning'></span>&nbsp;Budget for this month was already released");
		  $("#id_submit").attr("disabled", "disabled");
	      }else if (amount_bal.allowed=="no"){
		  $("#note").addClass("alert alert-danger").
		      html("Not allowed to issue fund release for this month, requirements from previous month must be submitted first");
		  $("#id_submit").attr("disabled", "disabled");
	      }else{
		  $("#note").addClass("alert alert-success").
		      html("After issuing this Fund Release Transmittal letter to the ORT will be generated");
		  $("#id_submit").removeAttr("disabled");
	      }
	  }
	 );
}


function viewFundStatDetails(agency, year, allocation){
    $.get('/agency/fund/view_fstat_detail', 
	  {'agency_id' : agency,
	   'year'      : year,
	   'allocation': allocation
	  },
	  function(data){
	     $('#fund_stat_detail').html(data);
	  }
	 );
}

function checkFundAmountRelease(){
    balance = new Number($("#balance").html());
    amount_release = new Number($("#id_amount").val());

    return amount_release<=balance;
}

function printNC(){
    $('#com_note').printArea();
}

function printTransNote(){
    $('#trans_note').printArea();
}


$('#id_ada').keydown(function(){
    return allNumbers(event);
});

$('#id_amount').keydown(function(){
    return Decimals(event);
});


$(document).ready(function(){
    var action = $('#action').val();
    if (action=="add"){
	getAllotmentBal();
    }

});

$('#id_allocation').change(function(){
    getAllotmentBal();
});

$('#id_month').change(function(){
    getAllotmentBal();
});

function getAllotmentBal(){
    var params = {'year'       : $('#year').val(),
		  'month'      : $('#id_month').val(),
		  'agency_id'  : $('#agency_id').val(),
		  'allocation' : $('#id_allocation').val()
		 }
    $.get('/agency/fund/allotment_balance',
	  params, 
	  function(data){
	      $('#id_amount').val(data);
	  }
	 );
}


function printNOT(){//notice of transmittal
    var agency = $('#agency').val();
    var oic = $('#oic').val();
    var content = $('#content').val();

    $('#content_letter').html(content);
    $('#oic_letter').html(oic);
    $('#trans_note').printArea();
}


function printNOC(){
    var agency = $('#agency').val();
    var oic = $('#oic').val();
    var content = $('#content').val();

    $('#compliance_content').html(content);
    $('#oic_letter').html(oic);
    $('#com_note').printArea();
}


/*monthly reports form ajax scripts*/
$("#id_year").change(function(){
    var data = {year    : $(this).val(),
	       month    : $("#id_month").val(),
	       agency_id: $("#agency_id").val()}

    $.get('/agency/unreported_activities', data, function(rs){
	$("#activity_select").html(rs);
    });

});


$("#id_month").change(function(){
    var data = {year    : $("#id_year").val(),
	       month    : $(this).val(),
	       agency_id: $("#agency_id").val()}

    $.get('/agency/unreported_activities', data, function(rs){
	$("#activity_select").html(rs);
    });
});

function showVariance(id){
    var target = $("#target"+id).html();
    var acc = $("#"+id).val();
    var diff = acc-target;

    if(diff==0){
	$("#variance"+id).html("<span>"+diff+"</span>");
    }else if (diff > 0){
	$("#variance"+id).html("<span class='text-success'>"+diff+"</span>");
    }else{
	$("#variance"+id).html("<span class='text-danger'>"+diff+"</span>");
    }
}

function showReportBalance(){
    var received = $("#received").val();
    var incurred = $("#incurred").val();
    var diff = received-incurred;
    if (diff==0){
	$("#remaining_bal").html("<span>"+diff+"</span>");
    }else if(diff>0){
	$("#remaining_bal").html("<span class='text-sucess'>"+diff+"</span>");
    }else{
	$("#remaining_bal").html("<span class='text-danger'>"+diff+"</span>");
    }
}



