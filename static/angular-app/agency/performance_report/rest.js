(function(){
  'use strict';

  angular
  .module('agency.services')
  .service('PerformanceReportREST', performanceReportREST);

  performanceReportREST.$inject = [
    '$http'
  ];

  function performanceReportREST(){

    this.url = '/rest/agency/performance_reports';

    this.list_all = function (){
      return $http.get(url);
    }

    this.list = function(){
      kljdsflkj
      sdsd
    }
  }

})();
