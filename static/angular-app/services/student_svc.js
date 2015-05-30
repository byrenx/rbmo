angular.module('app.services').service('StudentSvc', function($http){
    this.get_student_info = function(params){
	return $http.post("/registration/get/student_info", params);
    }
});
