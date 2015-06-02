angular.module('app.services').service('WFPSvc', function($http){
    
    this.getPerformanceReport = function(id){
	return $http.get('/get/performance_report/' + id);
    }
    
    this.updatePerformanceReport = function(params){
	return $http.post('/get/performance_report/', params);
    }

    this.getPerformanceIndicator = function(id){
	return $http.post('/get/performance_indicator' + id);
    }

    this.getPerformanceIndicator = function(id){
	return $http.post('/get/performance_indicator' + id);
    }
    


});
