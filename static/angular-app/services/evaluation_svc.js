angular.module('app.services').service('EvaluationSvc', function($http){
    this.getEvaluation = function(params){
	return $http.post('/registration/student_evaluation/',  params);
    }
    
    this.save_grades = function(params){
	return $http.post('/registration/student_old_grade', params);
    }

    this.get_grades = function(params){
	return $http.post('/registration/get/gradecard', params);
    }

    this.add_subject_grade = function(params){
	return $http.post('/registration/add/subject_grade', params);
    }

    this.del_subject_grade = function(params){
	return $http.post('/registration/del/subject_grade', params);
    }

    this.get_old_grade = function(params){
	return $http.post('/registration/get/subject_grade', params);
    }

    this.edit_old_grade = function(params){
	return $http.post('/registration/edit/old_grade', params);
    }

    this.get_old_average = function(params){
	return $http.post('/registration/get/old_average', params);
    }

    this.edit_old_average = function(params){
	return $http.post('/registration/edit/old_average', params);
    }
    //student subject services
    this.get_student_subject = function(params){
	return $http.post('/registration/get/student_subject', params);
    }

    this.edit_student_subject = function(params){
	return $http.post('/registration/edit/student_subject', params);
    }

});
