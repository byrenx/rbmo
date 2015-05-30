angular.module('app.services').service('WFPSvc', function($http){
    
    this.getEvaluation = function(params){
	return $http.post('//student_evaluation/',  params);
    }
    

});
