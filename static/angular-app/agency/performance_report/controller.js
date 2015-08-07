(function(angular){
    'use strict';

    angular
    .module('agency.controllers')
    .controller('PerformanceReportCtrl', performanceReportCtrl);

    performanceReportCtrl.$inject = [
	
    ];

    function performanceReportCtrl(){
	var vm = this;

	activate();

	function activate(){
	    console.log();
	}

    }
})(window.angular);
