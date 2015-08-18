(function(){
  'use strict';

  angular
  .module('agency.factory')
  .service('PerformanceReport', performanceReport);

  performanceReport.$inject = [
  ];

  function PerformanceReport(){
    function PerformanceReport(){
    }

    PerformanceReport.list = [];
    PerformanceReport.list_all = list_all;


    function list_all(){
      Property.list = [];
    }
  }
});
