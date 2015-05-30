angular.module('app.services').service('AgencySvc', function($http){
    
    this.getEvaluation = function(params){
	return $http.post('/registration/student_evaluation/',  params);
    }
    

});
