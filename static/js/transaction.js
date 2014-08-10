$('#filter_option').change(function(){
    var option = $(this).val();
    if (option=="month"){
	$('#date').attr('type', 'month');
    }else{
	$('#date').attr('type', 'date');
    }
});
