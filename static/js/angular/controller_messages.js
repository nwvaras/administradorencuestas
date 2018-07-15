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
    $scope.query = {
    order: 'titulo',
    limit: 5,
    page: 1
  };
  $scope.logOrder = function (property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    var a= function (a,b) {
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
    $scope.messages.sort(a)

  };

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
