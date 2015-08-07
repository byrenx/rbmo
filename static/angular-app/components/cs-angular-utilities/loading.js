angular.module('cs.loading', []).
directive('loading', ['$compile', function ($compile) {
  'use strict';
  return {
    restrict: 'EA',
    scope: {
      'instance': '=loading'
    },
    link: function($scope, elem, attrs){
      var $elem = $(elem);

      // $elem.addClass('hidden');
      $elem.fadeOut();

      $scope.$watch('instance.is_loading', function(v){
        if(v){
          // $elem.removeClass('hidden');
          $elem.fadeIn();
        } else {
          $elem.fadeOut();
          // $elem.addClass('hidden');
        }
      });
    }
  };
}]).
service('loading', function(){
  var complete = function(instance, q){
    return function(){
      instance._futures.splice(instance._futures.indexOf(q), 1);
      check(instance);
    };
  };

  var check = function(instance){
    instance.is_loading = !!instance._futures.length;
  };

  return {'new': function(){
    return {
      is_loading: false,
      _futures: [],
      watch: function($q){
        this._futures.push($q);
        $q.then(complete(this, $q), complete(this, $q));
        check(this);
        return $q;
      }
    };
  }};
});
