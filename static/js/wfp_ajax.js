var pi_lists = new List();

function getWFPData(wfp_id){
    $.get('/agency/wfp/wfpdetail', {'wfp_id':wfp_id}, function(data){
	$("#wfp_detail").html(data)
    });
}

function addPhysicalTarget(){
    var count = new Number($('#pi_count').val());
    var pi = $('#pi').val();
    var q1 = $('#q1').val();
    var q2 = $('#q2').val();
    var q3 = $('#q3').val();
    var q4 = $('#q4').val();

    if(count==0 && pi!=''){
	$('#pi-table').css('display', 'block');
    }
    if(pi!=''){
	if (pi_lists.found(pi)==false){
	
	    pi_lists.add(pi);
	    $('#pi-table-content').append("<tr id='"+count+"'><td><a href='javascript:removePIRow(\"" + count + "\",\"" + pi + "\")'><span class='glyphicon glyphicon-remove text-danger'></span></td>"
					  + "<input type='hidden' name='pis[]' value='" + pi +";"+ q1 +";"+ q2 +";"+ q3 +";"+ q4 +"'/>"
					  + "<td>" + pi 
					  + "</td><td>" + q1 
					  + "</td><td>" + q2 
					  + "</td><td>" + q3 
					  + "</td><td>" + q4 +"</tr>");
	    $('#pi_count').val(count+1);
	}else{
	    alert("'"+pi+"' already exist");
	}
    }
}

function removePIRow(row_id, pi){
    $('#'+row_id).remove();
    var count = new Number($('#pi_count').val());    
    if ((count-1)==0){
	$('#pi-table').css('display', 'none');
    }
    $('#pi_count').val((count-1));
    pi_lists.del(pi);
}


/*
  mpfro script
*/

var mpfro_list = new List();
var count_mpfro = 0;


function addAccTarget(){
   var pi = $('#pi').val();
   var pi_data = '';
   var pt = $('#pt').val();
   var acc = $('#acc').val();
   var variance = acc-pt;

   if (mpfro_list.found(pi)==false){

       mpfro_list.add(pi);
       $('#pi_acc').append("<tr id='"+count_mpfro+"'><td><a href='javascript:removePIAccRow(\"" + count_mpfro + "\",\"" + pi + "\")'><span class='glyphicon glyphicon-remove text-danger'></span></td>"
			   + "<input type='hidden' name='pis[]' value='" + pi +";"+ pt +";"+ acc +";"+ variance +";'/>"
			   + "<td>" + pi 
			   + "</td><td>" + pt 
			   + "</td><td>" + acc
			   + "</td><td>" + variance 
			   + "</td></tr>");
   }
}

function removePIAccRow(row_id, pi){
    $('#'+row_id).remove();
        
    if ((count_mpfro-1)==0){
	count_mpfro-=1;
    }
    mpfro_list.del(pi);
}


function setMonthlyTargetModal(id, month, amount){
    month_str = "";
    
    switch(month){
	case 1:
	  month_str = 'January';
	  break;
	case 2:
	  month_str = 'February';
	  break;
	case 3:
	  month_str = 'March';
	  break;
	case 4:
	  month_str = 'April';
	  break;
	case 5:
	  month_str = 'May';
	  break;
	case 6:
	  month_str = 'June';
	  break;
	case 7:
	  month_str = 'July';
	  break;
	case 8:
	  month_str = 'August';
	  break;
	case 9:
	  month_str = 'September';
	  break;
	case 10:
	  month_str = 'October';
	  break;
	case 11:
	  month_str = 'November';
	  break;
	case 12:
	  month_str = 'December';
	  break;
    }
    
    $('#id_wfp').val(id);
    $('#month').val(month);
    $('#amount').val(amount);
    $('#amount').focus();
    $('#myModalLabel').html(month_str);
}

function updateAmount(){
    data = {'id_wfp' : $('#id_wfp').val(),
	   'month'  : $('#month').val(),
	   'amount' : $('#amount').val()
	   }
    $.get('/agency/wfp/update_monthly_amount', data,
	  function(rs){
	      $('#monthlyModal').modal('hide');
	      getWFPData(data.id_wfp);
	  }
    );
}
