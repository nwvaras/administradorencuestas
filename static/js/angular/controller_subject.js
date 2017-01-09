'use strict';

var LOCALSTORAGE_ACTA_KEY = 'acta';

angular.module('DiscusionAbiertaApp').controller('ListCtrl', function($http,$scope, $mdDialog,$mdToast) {
  $scope.toppings = [
    { name: 'Edad minima', wanted: true },
    { name: 'Edad maxima', wanted: false },
    { name: 'Conjuntos', wanted: true },
    { name: 'Green Peppers', wanted: false }
  ];

  $scope.settings = [
    { name: 'Wi-Fi', extraScreen: 'Wi-fi menu', icon: 'device:network-wifi', enabled: true },
    { name: 'Bluetooth', extraScreen: 'Bluetooth menu', icon: 'device:bluetooth', enabled: false },
  ];

  $scope.messages = [
    {id: 1, title: "Message A", selected: false},
    {id: 2, title: "Message B", selected: true},
    {id: 3, title: "Message C", selected: true},
  ];

  $scope.people = [
    { name: 'Janet Perkins', newMessage: true },
    { name: 'Mary Johnson', newMessage: false },
    { name: 'Peter Carlsson', newMessage: false }
  ];
  $scope.selectedSurvey=""

  $scope.goToPerson = function(person, event) {
    $mdDialog.show(
      $mdDialog.alert()
        .title('Navigating')
        .textContent('Inspect ' + person)
        .ariaLabel('Person inspect demo')
        .ok('Neat!')
        .targetEvent(event)
    );
  };

  $scope.navigateTo = function(to, event) {
    $mdDialog.show(
      $mdDialog.alert()
        .title('Navigating')
        .textContent('Imagine being taken to ' + to)
        .ariaLabel('Navigation demo')
        .ok('Neat!')
        .targetEvent(event)
    );
  };

  $scope.doPrimaryAction = function(event) {
    $mdDialog.show(
      $mdDialog.alert()
        .title('Primary Action')
        .textContent('Primary actions can be used for one click actions')
        .ariaLabel('Primary click demo')
        .ok('Awesome!')
        .targetEvent(event)
    );
  };

  $scope.doSecondaryAction = function(event) {
    $mdDialog.show(
      $mdDialog.alert()
        .title('Secondary Action')
        .textContent('Secondary actions can be used for one click actions')
        .ariaLabel('Secondary click demo')
        .ok('Neat!')
        .targetEvent(event)
    );
  };
$scope.selected = [];
  $scope.subjects =[];
  $scope.filters={'filters': {
    'age-min' : 0,
    'age-max' : 99,
    'conjuntos' : [],
  }}

  var cargarDatos = function () {

    $http({
      method: 'POST',
      url: '/encuestas/subjects/',
      data: $scope.filters
    }).then(function (response) {

          $scope.subjects = response.data.usuarios;


    });

  };
  var cargarEncuestas= function () {

    $http({
      method: 'POST',
      url: '/encuestas/surveys/',
      data: { test: 'test' }
    }).then(function (response) {

          $scope.encuestas = response.data.encuestas;


    });
  }
  $scope.sendSurveys= function () {

    $http({
      method: 'POST',
      url: '/encuestas/surveys/send/',
      data: { encuesta:$scope.selectedSurvey,
      usuarios: $scope.selected}
    }).then(function (response) {

           afterChange()


    });
  }
  $scope.sendMessage=""
  $scope.createAndSendMessage= function () {

    $http({
      method: 'POST',
      url: '/encuestas/messages/create/',
      data: {message:$scope.sendMessage,
      users:$scope.selected}
    }).then(function (response) {

           afterChange()


    });
  }
  var afterChange= function (){
    console.log("yeah")
      cargarEncuestas()
    cargarDatos()
  }
 afterChange()
  $scope.test = true
  $scope.selectedRowCallback = function(rows){
            $mdToast.show(
                $mdToast.simple()
                    .content('Selected row id(s): '+rows)
                    .hideDelay(3000)
            );
        };
  $scope.getConjuntos= function(conjuntos) {
    var total =""
    for (var i = 0; i < conjuntos.length; i++) {
      var obj = conjuntos[i];
      total = total + " " + obj.name
    }
    return total
  }
  var DialogController = function ($scope, $mdDialog) {

  };
  $scope.createUser = function(ev) {


            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/cpadmin/encuestas/subject/add/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                fullscreen: true // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {

                });
        }
        ;
  $scope.editUser = function(user,ev) {


            $mdDialog.show({
                controller: DialogController,
                templateUrl: '/cpadmin/encuestas/subject/'+user.pk+'/change/',
                parent: angular.element(document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                fullscreen: true // Only for -xs, -sm breakpoints.
            })
                .then(function (answer) {

                });
        }
        ;

});
