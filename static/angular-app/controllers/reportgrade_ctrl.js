angular.module('app.controllers').controller('ReportGradeCtrl', function($scope, $log, ReportGradeSvc){

    $scope.students = [];
    $scope.section = {};
    $scope.report_filter = {};
    $scope.students = [];
    $scope.student_ids = [];
    
    //grade cards variable
    $scope.school_year = '';
    $scope.grade_cards = []; //holds the grade cards of many students
    $scope.grading_system = [{'grade': 'A', 'range': '96-100', 'def': 'Excellent'},
			     {'grade': 'A-', 'range': '93-95', 'def': 'Outstanding'},
			     {'grade': 'B+', 'range': '90-92', 'def': 'Very Good'},
			     {'grade': 'B-', 'range': '87-89', 'def': 'Good'},
			     {'grade': 'B', 'range': '84-86', 'def': 'Satisfactory'},
			     {'grade': 'C+', 'range': '81-83', 'def': 'Fair'},
			     {'grade': 'C-', 'range': '78-80', 'def': 'Pass'},
			     {'grade': 'C', 'range': '75-77', 'def': 'Poor Pass'},
			     {'grade': 'F', 'range': '74-Below', 'def': 'Failed'}
			    ];

    $scope.year_levels = ['Nursery', 'Kinder Junior', 'Kinder Senior',
			  'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 
			  'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8',
			  '1st Year Junior', '2nd Year Junior', '1st Year Senior',
			  '2nd Year Senior'];

    $scope.strDate = function(date){
	//requires moment.js
	return moment(date).format("MMMM D, YYYY");
    }
    //functions
    $scope.getAge = function(date){
	//requires calc.js
	return getAge(date);
    }

    $scope.level = function(level){
	if (level==0) return 'NURSERY';
	else if(level>=1 && level <=2) return 'KINDERGARTEN';
	else if(level>=3 && level <=10) return 'ELEMENTARY';
	else return 'HIGHSCHOOL';
    }

    $scope.rating = function(grade){
	if (grade >= 90) return 'A';
	else if(grade >=85 && grade <= 89) return 'P';
	else if(grade >= 80 && grade <= 84) return 'AP';
	else if(grade >= 75 && grade <= 79) return 'D';
	else return 'B';
    }

    $scope.getStudents = function(){
	$scope.report_filter['csrfmiddlewaretoken'] = $('[name="csrfmiddlewaretoken"]').val();
	ReportGradeSvc.getStudents($scope.report_filter)
	    .success(function(data, status){
		$scope.students = data.students;
		//$scope.load_ids($scope.students);
		$scope.section = data.section;
		$scope.school_year = data.school_year;
		$log.log(data);

		//clear selected student_ids
		$scope.student_ids = [];
	    })
	    .error(function(data, status){
		alert(data);
	    })
    }

    $scope.load_ids = function(students){
	$scope.student_ids = [];
	for(var i=0; i<$scope.students.length; i++)
	    $scope.student_ids.push($scope.students[i].id);
	$log.log($scope.student_ids);
    }

    //triggered when select all checkbox is clicked
    $scope.checkedAll = function(){
	$scope.check = !$scope.check;
	for(var i=0; i<$scope.students.length; i++){
	    $scope.students[i].selected = $scope.check;
	    if (!$scope.check){
		var index = $scope.student_ids.indexOf($scope.students[i].id);
		$scope.student_ids.splice(index, 1);
	    }
	}
    }


    $scope.check = false;
    $scope.selectAllStudents = function(){
	$scope.checkedAll();
	if ($scope.check){
	    $scope.load_ids();
	}
    }


    $scope.checkStudent = function(student){
	var index = $scope.students.indexOf(student);
	$scope.students[index].selected = !$scope.students[index].selected;

	if($scope.student_ids.indexOf(student.id) < 0 && $scope.students[index].selected == true){
	    $scope.student_ids.push(student.id);
	}else{
	    var id_index = $scope.student_ids.indexOf(student.id);
	    $scope.student_ids.splice(id_index, 1);
	}
	//check or uncheck all button
	if ($scope.student_ids.length === $scope.students.length){
	    $scope.check = true;
	}else{
	    $scope.check = false;
	}
	
    }


    $scope.genStudentGradeCards = function(){
	var request_params = {'section'    : $scope.report_filter.section,
			      'student_ids': $scope.student_ids};

	$("#printgcsbtn_id").html("<i class='fa fa-spinner fa-pulse'></i>&nbsp;Please Wait...");
	ReportGradeSvc.getStudentGradeCards(request_params)
	    .success(function(data, status){
		$scope.grade_cards = data.grade_cards;
		$log.log($scope.grade_cards);
		setTimeout(function(){
		    $("#printgcsbtn_id").html("<span class='glyphicon glyphicon-print' id='printgcs_id'></span>&nbsp;Grade Card");		    

		    $("#grade_cards_print").printArea();
		}, 3000);

	    })
	    .error(function(data, status){
		
	    });
    }

    $scope.generateGradeSlip = function(){
	var request_params = {'section'    : $scope.report_filter.section,
			      'student_ids': $scope.student_ids};
	ReportGradeSvc.getStudentGradeCards(request_params)
	    .success(function(data, status){
		$scope.grade_cards = data.grade_cards;
		$log.log($scope.grade_cards);
		setTimeout(function(){
		    $('#gradeslip_print').printArea();
		}, 2000);

	    })
	    .error(function(data, status){
		
	    });
    }
});
