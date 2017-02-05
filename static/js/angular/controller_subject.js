'use strict';

var LOCALSTORAGE_ACTA_KEY = 'acta';

angular.module('DiscusionAbiertaApp').controller('ListCtrl', function($http,$scope, $mdDialog,$mdToast,$window) {
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
  var last = {
      bottom: true,
      top:  false,
      left: false,
      right: true
    };

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
  $scope.toastPosition = angular.extend({},last);

  $scope.getToastPosition = function() {
    sanitizePosition();

    return Object.keys($scope.toastPosition)
      .filter(function(pos) { return $scope.toastPosition[pos]; })
      .join(' ');
  };

  function sanitizePosition() {
    var current = $scope.toastPosition;

    if ( current.bottom && last.top ) current.top = false;
    if ( current.top && last.bottom ) current.bottom = false;
    if ( current.right && last.left ) current.left = false;
    if ( current.left && last.right ) current.right = false;

    last = angular.extend({},current);
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

            $window.location.href ='/admin/encuestas/subject/add/';
  }

  $scope.editUser = function(user,ev) {

            $window.location.href = '/admin/encuestas/subject/'+user.pk+'/change/';


}
  $scope.files = ""
  $scope.$watch('files.length',function(newVal,oldVal){
          console.log($scope.files[0]);
            uploadCSV($scope.files[0]);
  });


  function DialogConjunto($scope, $mdDialog) {
    $scope.hide = function() {
      $mdDialog.hide();
    };

    $scope.no = function() {
      $mdDialog.cancel();
    };

    $scope.enviar = function() {
      $mdDialog.hide('enviado');
    };
  }
    $scope.loadSurveyDetail = function(survey){
        $window.location.href = '/encuestas/surveys/info/' + survey.pk;
    }
    $scope.showDialogMessage= function(ev) {
    $mdDialog.show({
      controller: DialogConjunto,
      templateUrl: '/static/html/angular/cargar_conjunto_final4.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      fullscreen: true // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
          console.log("subido")
          console.log($scope.files)
          uploadCSV($scope.files[0])
    }, function() {
           console.log("no subido")
      $scope.status = 'You cancelled the dialog.';
    });
  };

  var uploadCSV= function (file) {
    var formData = new FormData();
            angular.forEach($scope.files,function(obj){
                if(!obj.isRemote){
                    formData.append('csv', obj.lfFile);
                }
            });

         $http.post('/encuestas/subjects/fromcsv/', formData, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            }).then(function(result){
            //$mdDialog.hide();

                 $scope.sendToast('Conjuntos cargados con exito')
            },function(err){
           //$mdDialog.hide();
                $scope.sendToast('Error al cargar conjuntos')
            });

  }

  $scope.sendToast = function(message) {
    var pinTo = $scope.getToastPosition();

    $mdToast.show(
      $mdToast.simple()
        .textContent(message)
        .position(pinTo )
        .hideDelay(3000)
    );
  };
});
