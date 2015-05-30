angular.module('app.controllers').controller('EvaluationCtrl', function($scope, $log, $modal, EvaluationSvc, StudentSvc){
    $scope.level_types = [{'val': 1, 'text': 'Nursery' },
			  {'val': 2, 'text': 'Kinder' },
			  {'val': 3, 'text': 'Elementary(Old)' },
			  {'val': 4, 'text': 'HighSchool(Old)' },
			  {'val': 5, 'text': 'Elementary(New)' },
			  {'val': 6, 'text': 'HighSchool(New)' }];

    $scope.evaluation_params = {};
    $scope.evaluation = {};
    $scope.grades = [];

    $scope.strDate = function(date, format){
	//requires moment.js
	return moment(date).format(format);
    }

    $scope.getEvaluation = function(){
	$scope.evaluation_params['csrfmiddlewaretoken'] = $('[name="csrfmiddlewaretoken"]').val();
	$log.log($scope.evaluation_params);

	EvaluationSvc.getEvaluation($scope.evaluation_params)
	    .success(function(data, status){
		$scope.evaluation = data;
		$log.log(data);
	    })
	    .error(function(data, status){
		$log.log(data);
	    })
    }

    $scope.getStudentInfo = function(id){
	StudentSvc.get_student_info({'id': id})
	    .success(function(data, status){
		$scope.student = data;
	    })
	    .error(function(data, status){
		$log.log(data);
	    });
    }

    $scope.showGradeCardPrintDiag = function(studentid, year_level){
	var params = {'student_id' : studentid,
		      'year_level' : year_level};
	
	EvaluationSvc.get_grades(params)
	    .success(function(data, status){
		$log.log(data);
		$scope.student = data.student;
		$scope.subject_grade = data.subject_grade;
		$("#grade_card_print").printArea();
	    })
	    .error(function(data, status){
		//$log.log(data);
	    })
    }


    //delete old_subject grade
    $scope.delete_subject = function(id, table_ref){
	EvaluationSvc.del_subject_grade({'id': id, 'table_ref': table_ref})
	    .success(function(data, status){
		if (status == 200){
		    $scope.getEvaluation();
		}
	    })
	    .error(function(data, status){
		$log.log(data);
	    });
    }

    $scope.items = [1, 2, 3];
    //modal for grade entry
    $scope.openTransferreGradeEntryModal = function(year_level, student_id){
	var modalInstance = $modal.open({
	    templateUrl: '/static/angular-app/templates/evaluation/transferre_grade_form.html',
	    controller: 'TranferreModalInstanceCtrl',
	    size: 'lg',
	    resolve: {
		items: function () {
		    return {'year_level': year_level, 'student_id': student_id};
		}
	    }
	});

	modalInstance.result.then(function (selectedItem) {
	    $scope.selected = selectedItem;
	    //$scope.getEvaluation();
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	    $scope.getEvaluation();
	});
    }


    //modal for adding subject grade
    $scope.openAddSubjectGradeModal = function(table_ref, school_year, year_level, student_id){
	var modalInstance = $modal.open({
	    templateUrl: '/static/angular-app/templates/evaluation/subject_grade_form.html',
	    controller: 'AddSubjectGradeCtrl',
	    size: 'lg',
	    resolve: {
		items: function () {
		    return {'table_ref': table_ref,
			    'school_year': school_year,
			    'year_level': year_level, 
			    'student_id': student_id};
		}
	    }
	});

	modalInstance.result.then(function (selectedItem) {
	    $scope.selected = selectedItem;
	    //$scope.getEvaluation();
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	    $scope.getEvaluation();
	});
    }

    //modal for editing old subject grade
    $scope.openEditSubjectGradeModal = function(id){
	var modalInstance = $modal.open({
	    templateUrl: '/static/angular-app/templates/evaluation/edit_grade_form.html',
	    controller: 'EditSubjectGradeCtrl',
	    size: 'lg',
	    resolve: {
		items: function () {
		    return {'id': id};
		}
	    }
	});

	modalInstance.result.then(function (selectedItem) {
	    $scope.selected = selectedItem;
	    //$scope.getEvaluation();
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	    $scope.getEvaluation();
	});
    }

    //modal for editing old average grade
    $scope.openEditAverageGradeModal = function(id){
	var modalInstance = $modal.open({
	    templateUrl: '/static/angular-app/templates/evaluation/edit_old_grade_average_form.html',
	    controller: 'EditAverageGradeCtrl',
	    size: 'md',
	    resolve: {
		items: function () {
		    return {'id': id};
		}
	    }
	});

	modalInstance.result.then(function (selectedItem) {
	    $scope.selected = selectedItem;
	    //$scope.getEvaluation();
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	    $scope.getEvaluation();
	});
    }


    //edit student subject modal form event
    $scope.openEditStudentSubjectModal = function(id){
	var modalInstance = $modal.open({
	    templateUrl: '/static/angular-app/templates/evaluation/edit_student_subject_grade_form.html',
	    controller: 'EditStudentSubjectGradeCtrl',
	    size: 'md',
	    resolve: {
		items: function () {
		    return {'id': id};
		}
	    }
	});

	modalInstance.result.then(function (selectedItem) {
	    $scope.selected = selectedItem;
	    //$scope.getEvaluation();
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	    $scope.getEvaluation();
	});
    }//end of edit student subject modal form event
    

});


angular.module('app.controllers').controller('TranferreModalInstanceCtrl', function($scope, $modalInstance, $log, items, EvaluationSvc, SubjectSvc){

    $scope.grade = {};
    $scope.year_grades = {};
    $scope.year_levels = ['Nursery', 'Kinder Junior', 'Kinder Senior',
			  'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 
			  'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8',
			  '1st Year Junior', '2nd Year Junior', '1st Year Senior',
			  '2nd Year Senior'];
    $scope.year_level_desc = $scope.year_levels[items.year_level-1];
    $log.log(items.year_level);
    $scope.grades_entered = [];
    $log.log(items.student_id);
    $scope.Subjects = [];

    $scope.school_year = {};


    $scope.adding_done = false;
    $scope.adding_state = true;
    //fetch all subjects for this year_level
    SubjectSvc.fetch_subjects({'year_level': items.year_level})
	.success(function(data, status){
	    $scope.subjects = data;
	    $log.log(data);
	})
	.error(function(data, status){
	    $log.log(data);
	});

    //validator functions
    //requires input_validator.js
    $scope.numbers = function(){
	return allNumbers();
    }
    //set school_year
    $scope.setSchoolYear = function(){
	$log.log($scope.school_year_from);
	$scope.year_grades['school_year'] = $scope.school_year_from + '-' + ($scope.school_year_from+1);
	$log.log($scope.year_grades['school_year']);
    }


    $scope.add_subject = function(){
	var new_grade = $scope.grade;
	$log.log(new_grade);
	if ($scope.grades_entered.indexOf(new_grade) < 0 && !($scope.isEmpty(new_grade))){
	    $scope.grades_entered.push(new_grade);
	    $scope.grade = {};
	}
    }

    $scope.isEmpty = function (obj) {
	if (Object.keys(obj).length === 0){
	    return true;
	}else if(obj.subject === '' || obj.q1 == null || obj.q2 == null || obj.q3 == null || obj.q4 == null || obj.final == null || obj.units == null){
	    return true;
	}else{
	    return false;
	}
	
    }

    $scope.editSubject = function(subject){
	var index = $scope.grades_entered.indexOf(subject);
	$scope.grade = $scope.grades_entered[index];
    }
    //remove the subject grade from the list
    $scope.deleteSubject = function(subject){
	var index = $scope.grades_entered.indexOf(subject);
	$scope.grades_entered.splice(index, 1);
    }

    $scope.save = function(){
	$scope.year_grades['student_id'] = items.student_id;
	$scope.year_grades['year_level'] = items.year_level;
	$scope.year_grades['grades'] = $scope.grades_entered;
	$scope.year_grades['school_year'] = $scope.school_year.from + '-' + ($scope.school_year.from+1);
	$log.log($scope.year_grades['school_year']);
	//$modalInstance.close('sas');
	if($scope.year_grades.school == null || $scope.year_grades.school === ''){
	    $("#school").focus();
	}else if($scope.school_year.from == null || $scope.school_year.from === ''){
	    $("#school_year_from").focus();
	}else if($scope.year_grades.average == null || $scope.year_grades.average === ''){
	    $("#average").focus();
	}else{
	    $("#save_grade_id").attr('disabled', 'disabled');
	    $("#save_grade_id").html("<i class='fa fa-spinner fa-pulse'></i>&nbsp;Saving...");

	    EvaluationSvc.save_grades($scope.year_grades)
		.success(function(data, status){
		    setTimeout(function(){
			$("#save_grade_id").removeAttr('disabled');
			$("#save_grade_id").html("Save");
		    }, 2000);
		    $log.log(data);
		    $scope.adding_state = false;
		    $scope.adding_done = true;

		})
		.error(function(data, status){
		    $log.log(data);
		})

	}


    }

    $scope.cancel = function(){
	$modalInstance.dismiss('cancel');
    }
});

//add sbject grade form controller
angular.module('app.controllers').controller('AddSubjectGradeCtrl', function($scope, $modalInstance, $log, items, EvaluationSvc, SubjectSvc){
    $scope.adding_state = true;
    $scope.adding_done = false;

    $scope.grade = {};
    $scope.year_grades = {};
    $scope.year_levels = ['Nursery', 'Kinder Junior', 'Kinder Senior',
			  'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 
			  'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8',
			  '1st Year Junior', '2nd Year Junior', '1st Year Senior',
			  '2nd Year Senior'];
    $scope.year_level_desc = $scope.year_levels[items.year_level-1];
    $log.log(items.year_level);
    $scope.grades_entered = [];
    $log.log(items.student_id);
    $scope.Subjects = [];
    $scope.adding_done = false;
    $scope.adding_state = true;

    //fetch all subjects for this year_level
    SubjectSvc.fetch_subjects({'year_level': items.year_level})
	.success(function(data, status){
	    $scope.subjects = data;
	    $log.log(data);
	})
	.error(function(data, status){
	    $log.log(data);
	});


    $scope.add_subject = function(){
	var new_grade = $scope.grade;
	$log.log(new_grade);

	if ($scope.grades_entered.indexOf(new_grade) < 0 && !($scope.isEmpty(new_grade))){
	    $scope.grades_entered.push(new_grade);
	    $scope.grade = {};
	}
    }

    $scope.isEmpty = function (obj) {
	if (Object.keys(obj).length === 0){
	    return true;
	}else if(obj.subject === '' || obj.q1 == null || obj.q2 == null || obj.q3 == null || obj.q4 == null || obj.final == null || obj.units == null){
	    return true;
	}else{
	    return false;
	}
	
    }

    $scope.editSubject = function(subject){
	var index = $scope.grades_entered.indexOf(subject);
	$scope.grade = $scope.grades_entered[index];
    }
    //remove the subject grade from the list
    $scope.deleteSubject = function(subject){
	var index = $scope.grades_entered.indexOf(subject);
	$scope.grades_entered.splice(index, 1);
    }

    $scope.save = function(){
	$scope.year_grades['student_id'] = items.student_id;
	$scope.year_grades['year_level'] = items.year_level;
	$scope.year_grades['grades'] = $scope.grades_entered;
	$scope.year_grades['school_year'] = items.school_year;
	$scope.year_grades['table_ref'] = items.table_ref;
	//$modalInstance.close('sas');

	$("#save_grade_id").attr('disabled', 'disabled');
	$("#save_grade_id").html("<i class='fa fa-spinner fa-pulse'></i>&nbsp;Saving...");

	EvaluationSvc.add_subject_grade($scope.year_grades)
	    .success(function(data, status){
		if (status == 200){
		    setTimeout(function(){
			$("#save_grade_id").removeAttr('disabled');
			$("#save_grade_id").html("Save");
		    }, 2000);
		    $log.log(data);
		    $scope.adding_state = false;
		    $scope.adding_done = true;
		}

	    })
	    .error(function(data, status){
		$log.log(data);
	    })
	
    }

    $scope.cancel = function(){
	$modalInstance.dismiss('cancel');
    }

});

angular.module('app.controllers').controller('EditSubjectGradeCtrl', function($scope, $modalInstance, $log, items, EvaluationSvc, SubjectSvc){
    $scope.grade = {};

    
    $scope.adding_done = false;
    $scope.adding_state = true;

    EvaluationSvc.get_old_grade({'id': items.id})
	.success(function(data, status){
	    $scope.grade = data;
	})
	.error(function(data, status){
	    $log.log(data);
	});


    $scope.save = function(){
	EvaluationSvc.edit_old_grade($scope.grade)
	    .success(function(data, status){
		if (status==200){
		    $scope.adding_done = true;
		    $scope.adding_state = false;
		}
	    })
	    .error(function(data, status){
		$log.log(data);
	    });
    }

    $scope.cancel = function(){
	$modalInstance.dismiss('cancel');
    }

});

//edit average grade modal
angular.module('app.controllers').controller('EditAverageGradeCtrl', function($scope, $modalInstance, $log, items, EvaluationSvc, SubjectSvc){
    $scope.grade = {};

    
    $scope.adding_done = false;
    $scope.adding_state = true;

    EvaluationSvc.get_old_average({'id': items.id})
	.success(function(data, status){
	    $scope.grade = data;
	    $log.log($scope.grade);
	})
	.error(function(data, status){
	    $log.log(data);
	});


    $scope.save = function(){
	EvaluationSvc.edit_old_average($scope.grade)
	    .success(function(data, status){
		if (status==200){
		    $scope.adding_done = true;
		    $scope.adding_state = false;
		}
	    })
	    .error(function(data, status){
		$log.log(data);
	    });
    }

    $scope.cancel = function(){
	$modalInstance.dismiss('cancel');
    }

});

angular.module('app.controllers').controller('EditStudentSubjectGradeCtrl', function($scope, $modalInstance, $log, items, EvaluationSvc, SubjectSvc){
    $scope.grade = {};

    
    $scope.adding_done = false;
    $scope.adding_state = true;

    EvaluationSvc.get_student_subject({'id': items.id})
	.success(function(data, status){
	    $scope.grade = data;
	    $log.log($scope.grade);
	})
	.error(function(data, status){
	    $log.log(data);
	});


    $scope.save = function(){
	EvaluationSvc.edit_student_subject($scope.grade)
	    .success(function(data, status){
		if (status==200){
		    $scope.adding_done = true;
		    $scope.adding_state = false;
		}
	    })
	    .error(function(data, status){
		$log.log(data);
	    });
    }

    $scope.cancel = function(){
	$modalInstance.dismiss('cancel');
    }

});




