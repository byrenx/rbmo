var pi_lists = new List();

function getWFPData(wfp_id){
    $.get('/agency/wfp/wfpdetail', {'wfp_id':wfp_id}, function(data){
	$("#wfp_detail").html(data);
s    });
}

function addPhysicalTarget(){
    var count = new Number($('#pi_count').val());
    var pi = $('#pi').val();
    var jan = ($('#pt1').val()==""? 0: $('#pt1').val());
    var feb = ($('#pt2').val()==""? 0: $('#pt2').val());
    var mar = ($('#pt3').val()==""? 0: $('#pt3').val());
    var apr = ($('#pt4').val()==""? 0: $('#pt4').val());
    var may = ($('#pt5').val()==""? 0: $('#pt5').val());
    var jun = ($('#pt6').val()==""? 0: $('#pt6').val());
    var jul = ($('#pt7').val()==""? 0: $('#pt7').val());
    var aug = ($('#pt8').val()==""? 0: $('#pt8').val());
    var sept = ($('#pt9').val()==""? 0: $('#pt9').val());
    var oct = ($('#pt10').val()==""? 0: $('#pt10').val());
    var nov = ($('#pt11').val()==""? 0: $('#pt11').val());
    var dec = ($('#pt12').val()==""? 0: $('#pt12').val());

    if(pi!=''){
	//pi_lists.add(pi);
	$('#pi-table-content').append("<tr id='"+count+"'><td><a href='javascript:removePIRow(\"" + count + "\",\"" + pi + "\")'><span class='glyphicon glyphicon-remove text-danger'></span></td>"
				      + "<input type='hidden' name='pis[]' value='" + pi + ";" + jan +";"+ feb +";"+ mar +";"+ apr +";"+ may +";"+ jun + ";" + jul + ";" + aug + ";" + sept + ";" + oct + ";" + nov + ";" + dec + "'/>"
				      + "<td>" + pi 
				      + "</td><td>" + jan 
				      + "</td><td>" + feb 
				      + "</td><td>" + mar 
				      + "</td><td>" + apr 
				      + "</td><td>" + may 
				      + "</td><td>" + jun 
				      + "</td><td>" + jul 
				      + "</td><td>" + aug 
				      + "</td><td>" + sept 
				      + "</td><td>" + oct 
				      + "</td><td>" + nov 
				      + "</td><td>" + dec +"</td></tr>");
	$('#pi_count').val(count+1);
    }
}

function removePIRow(row_id, pi){
    $('#'+row_id).remove();
    var count = new Number($('#pi_count').val());    
    $('#pi_count').val((count-1));
  //  pi_lists.del(pi);
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

    mpfro_list.add(pi);
    $('#pi_acc').append("<tr id='"+count_mpfro+"'><td><a href='javascript:removePIAccRow(\"" + count_mpfro + "\",\"" + pi + "\")'><span class='glyphicon glyphicon-remove text-danger'></span></td>"
			+ "<input type='hidden' name='pis[]' value='" + pi +";"+ pt +";"+ acc +";"+ variance +";'/>"
			+ "<td>" + pi 
			+ "</td><td>" + pt 
			+ "</td><td>" + acc
			+ "</td><td>" + variance 
			+ "</td></tr>");
}

function removePIAccRow(row_id, pi){
    $('#'+row_id).remove();
/*        
    if ((count_mpfro-1)==0){
	count_mpfro-=1;
    }
    mpfro_list.del(pi);
*/
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

function setActivityModal(wfp_id, major_program, allocation){
    $('#wfp_id').val(wfp_id);
    activity = $('#td'+wfp_id).html();
    $('#activity').val(activity);
    $('#program').val(major_program);
    $('#allocation').val(allocation);
}

function updateActivity(){
    var data = {'wfp_id'        : $('#wfp_id').val(),
		'activity'      : $('#activity').val(),
		'program'       : $('#program').val(),
		'allocation'    : $('#allocation').val()
	       }
    $.get('/agency/wfp/update_activity', data, function(rs){
	agency_id = $('#agency_id').val();
	window.location = "/agency/wfp/wfpinfo/"+agency_id+"/";
	//$('#td'+data.wfp_id).html(rs);
	//$('#close_activity_modal').click();
    });
}

function delPerfTarget(id, wfp_id){
    $.get('/agency/wfp/delete_perf_target', {'id': id}, function(rs){
	rs = new String(rs).trim();
	if (rs=='Deleted'){
	    getWFPData(wfp_id);
	}
    });
}


/***
    physical performance target 
**/
function addPerfTarget(){
    data = {'id_wfp' : $('#id_wfp').val(),
	    'pi' : $('#pi').val(),
	    'jan' : ($('#jan').val()==""? 0: $('#jan').val()),
	    'feb' : ($('#feb').val()==""? 0: $('#feb').val()),
	    'mar' : ($('#mar').val()==""? 0: $('#mar').val()),
	    'apr' : ($('#apr').val()==""? 0: $('#apr').val()),
	    'may' : ($('#may').val()==""? 0: $('#may').val()),
	    'jun' : ($('#jun').val()==""? 0: $('#jun').val()),
	    'jul' : ($('#jul').val()==""? 0: $('#jul').val()),
	    'aug' : ($('#aug').val()==""? 0: $('#aug').val()),
	    'sept' : ($('#sept').val()==""? 0: $('#sept').val()),
	    'oct' : ($('#oct').val()==""? 0: $('#oct').val()),
	    'nov' : ($('#nov').val()==""? 0: $('#nov').val()),
	    'dec' : ($('#dec').val()==""? 0: $('#dec').val())
	   }
    $.get('/agency/wfp/add_performance_target', 
	  data,
	  function(rs){
	      rs = new String(rs).trim();
	      if (rs=='Added'){
		  $('#pi_close_modal').click();
		  getWFPData(data.id_wfp);
	      }
	  }
	 );
}



function getPerformanceTarget(){
    var data = {'activity' : $('#activity').val(),
		'year'     : $('#year').val(),
		'month'    : $('#month').val()
	       }
    $.get('/agency/wfp/get_performance_acc', data, function(rs){
       $('#performance').html(rs);	
    });
}


function fillPhsTarget(month){
    month = new Number(month);
    var cur_val = $('#pt'+month).val();
    for(var i = month+1; i<=12; i++){
	$('#pt'+i).val(cur_val);
    }
}

function fillFinTarget(month){
    var months = ['id_jan','id_feb','id_mar','id_apr','id_may',
		  'id_jun','id_jul','id_aug','id_sept','id_oct',
		  'id_nov','id_dec'
		 ]
    month = new Number(month)-1;
    var cur_val = $('#'+months[month]).val();
    for(var i = month+1; i<=12; i++){
	$('#'+months[i]).val(cur_val);
    }
}


function delActivity(){
    var activity_id = $('#activity_id').val();
    var agency_id = $('#agency_id').val();
    $.get('/agency/wfp/delete_activity'
	 ,
	 {'activity_id': activity_id}
	 ,
	 function(rs){
	     window.location = '/agency/wfp/wfpinfo/'+ agency_id+"/";
	     
	 }
	);
}
