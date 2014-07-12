function removeReqMode(tag_id, req_sub_id){
    $('#'+tag_id+' span').removeClass().addClass('glyphicon glyphicon-remove text-danger');
}

function viewReqStatmode(tag_id){
    $('#'+tag_id+' span').removeClass().addClass('glyphicon glyphicon-check text-success');
}


function removeMonthlyReqMode(tag_id, req_sub_id){
    $('#'+tag_id+' span').removeClass().addClass('glyphicon glyphicon-remove text-danger');
}
