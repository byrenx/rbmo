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
    getAllotmentBal();
});

$('#allocation').change(function(){
    getAllotmentBal();
});

$('#id_month').change(function(){
    getAllotmentBal();
});

function getAllotmentBal(){
    var params = {'year'       : $('#year').val(),
		  'month'      : $('#id_month').val(),
		  'agency_id'  : $('#agency_id').val(),
		  'allocation' : $('#allocation').val()
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
