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
        cargarDatos()
           console.log(response)


    });
  }
    $scope.selected=[]
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
    $scope.editMessage = function(message,ev) {

            $window.location.href = '/admin/encuestas/message/'+message.pk+'/change/';


}
});
