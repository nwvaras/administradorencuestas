/**
 * Created by Nicolas on 01-01-2017.
 */
angular.module('DiscusionAbiertaApp').controller('MainCtrl', function($scope, $mdDialog,$http,$window){
    $scope.toppings = [
    { name: 'Pepperoni', wanted: true },
    { name: 'Sausage', wanted: false },
    { name: 'Black Olives', wanted: true },
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

    var cargarDatos = function () {

    $http({
      method: 'POST',
      url: '/encuestas/surveys/',
      data: { test: 'test' }
    }).then(function (response) {

          $scope.encuestas = response.data.encuestas;


    });

  };
    $scope.sendSurveys= function () {

    $http({
      method: 'POST',
      url: '/encuestas/surveys/sendFromSurvey/',
      data: { encuesta:$scope.selectedSurvey,
          selected: $scope.selected
                }
    }).then(function (response) {
            afterChange()
           console.log(response)


    });
  }
    $scope.createSurvey=""
    $scope.createAndSendSurvey= function () {
    $scope.createSurvey.encuesta.date=$scope.createSurvey.encuesta.date.toUTCString()
    $http({
      method: 'POST',
      url: '/encuestas/surveys/create/',
      data: $scope.createSurvey
    }).then(function (response) {
            afterChange()
           console.log(response)


    });
  }
    $scope.createAndSendMessage= function () {

    $http({
      method: 'POST',
      url: '/encuestas/messages/create/',
      data: {message:$scope.sendMessage,
      surveys:$scope.selected}
    }).then(function (response) {

           console.log(response)


    });
  }
    var afterChange= function (){
    console.log("yeah")
    cargarDatos()
  }
    $scope.filterSurvey = function(survey) {
        console.log("asd")
        return !(survey.estado[0].y == 0 &&survey.estado[1].y == 0 );
    };
    $scope.selected=[]
    afterChange()
 $scope.options = {
            chart: {
                type: 'pieChart',
                height: 150,
                donut: true,
                x: function(d){return d.key;},
                y: function(d){return d.y;},
                showLabels: true,
                showLegend: false,

                pie: {
                    startAngle: function(d) { return d.startAngle/2 -Math.PI/2 },
                    endAngle: function(d) { return d.endAngle/2 -Math.PI/2 }
                },
                duration: 20,

            }
        };
    $scope.query = {
    order: 'titulo',
    limit: 5,
    page: 1
  };
    var DialogController = function ($scope, $mdDialog) {

    $scope.aceptamos = false;

    $scope.aceptan = function () {
      $mdDialog.hide();
    };

    $scope.rechazan = function () {
      $mdDialog.cancel();
    };
  };
    $scope.loadSurveyDetail = function(survey){
        $window.location.href = '/encuestas/surveys/info/' + survey.pk;
    }

    $scope.showAdvanced = function(ev) {
        if ($scope.selected.length == 1) {
            var sel = $scope.selected[0]
            $window.location.href = '/admin/encuestas/survey/'+sel.pk+'/change/';
        }

    }
});