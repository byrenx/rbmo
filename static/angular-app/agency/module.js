(function(angular) {
    'use strict';

    angular
	.module('cs.utilities', [
	    'cs.pubsub',
	    'cs.passive-messenger',
	    'cs.loading',
	    'cs.modal',
	]);

    angular
	.module('agency.services', [
	    'cs.utilities',
	]);

    angular
	.module('agency.controllers', [
	    'agency.services',
	]);

    angular
	.module('agency.directives', [
	    'cs.utilities',
	]);

    angular
	.module('agency', [
	    'agency.services',
	    'agency.directives',
	    'agency.controllers',
	    'ngRoute',
	    'ngSanitize',
	    'ui.select',
	    'ui.materialize',
	])
	.run(agency);

    agency.$inject = ['$log', 'passive_messenger', '$timeout', '$rootScope'];

    function agency($log, passive_messenger, $timeout, $rootScope) {
	$log.info('Angular Agency Loaded');
	$timeout(function() { passive_messenger.success('Loaded'); });
	$rootScope.ngLoadingFinished = true;
    }
})(window.angular);
