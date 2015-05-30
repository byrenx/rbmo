angular.module('app.services').service('SubjectSvc', function($http){
    this.fetch_subjects = function(params){
	return $http.post('/registration/subjects',  params);
    }

});
