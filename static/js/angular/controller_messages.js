'use strict';

var LOCALSTORAGE_ACTA_KEY = 'acta';

angular.module('DiscusionAbiertaApp').controller('ListCtrl', function($http,$scope, $mdDialog,$mdToast,$window) {
    $scope.createAndSendMessage= function () {

    $http({
      method: 'POST',
      url: '/encuestas/messages/create/',
      data: {message:$scope.sendMessage,
      users:$scope.selected}
    }).then(function (response) {

           console.log(response)


    });
  }
    $scope.sendMessage =""

  var cargarDatos = function () {

    $http({
      method: 'POST',
      url: '/encuestas/mensajes/',
      data: { test: 'test' }
    }).then(function (response) {

          $scope.messages = response.data.mensajes;
        console.log(response)


    });

  };
    $scope.loadMessageDetail = function(survey){
        $window.location.href = '/encuestas/messages/info/' + survey.pk;
    }

    cargarDatos()
    $scope.showAdvanced = function(ev) {
        if ($scope.selected.length == 1) {
            var sel = $scope.selected[0]

            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/cpadmin/encuestas/survey/'+sel.pk+'/change/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                fullscreen: true // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {

                })
        }
        ;
    }
});
