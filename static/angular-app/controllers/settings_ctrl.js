angular.module('app.controllers').controller('SettingsCtrl', function($scope, $log, $modal){

    $scope.items = [1, 2, 3];
    $scope.openSettingsModal = function(){
	var modalInstance = $modal.open({
	    templateUrl: '/static/angular-app/templates/settings/settings_form.html',
	    controller: 'SettingsModalInstanceCtrl',
	    size: 'md',
	    resolve: {
		items: function () {
		    return $scope.items;
		}
	    }
	});

	modalInstance.result.then(function (selectedItem) {
	    $scope.selected = selectedItem;
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	});
    }

});


angular.module('app.controllers').controller('SettingsModalInstanceCtrl', function($scope, $modalInstance, $log, items){
    
    
});
