angular.module('app.controllers', []);
angular.module('app.services', []);


var app = angular.module("app", ['app.controllers', 'app.services', 'ui.bootstrap']).config(function($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
