angular.module('app.services').service('ReportGradeSvc', function($http){
    this.getStudents = function(params){
	return $http.post('/registration/get/students/section',  params);
    }

    this.getStudentGradeCards = function(params){
	return $http.post('/registration/get/students/gradecards', params);
    }
    
});
