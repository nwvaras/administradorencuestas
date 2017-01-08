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
    $scope.surveyDetails = pre.surveyDetails

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
    $scope.getConjuntos= function(conjuntos) {
    var total =""
    for (var i = 0; i < conjuntos.length; i++) {
      var obj = conjuntos[i];
      total = total + " " + obj.name
    }
    return total
  }
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
    $scope.totalConjuntos = ""
    var getDBConjuntos = function () {

    $http({
      method: 'GET',
      url: '/encuestas/conjuntos/'
    }).then(function (response) {

           console.log(response)
        $scope.totalConjuntos = response.data.conjuntos


    });
  }
    getDBConjuntos()

    $scope.getSended = true
    $scope.$watch('getSended', function() {
        console.log("watche")
        $scope.userTableinit()
    })
    $scope.getNotSended = true
    $scope.$watch('getNotSended', function() {
        console.log("watche")
        $scope.userTableinit()
    })
    $scope.getResponded = true
    $scope.$watch('getResponded', function() {
        console.log("watche")
        $scope.userTableinit()
    })
    $scope.getNotResponded = true
    $scope.$watch('getNotResponded', function() {
        console.log("watche")
        $scope.userTableinit()
    })
    $scope.conjuntosFilter= function(x) {
        var conjuntos = x.conjuntos
        var total = true
       for (var i = 0; i < conjuntos.length; i++) {
           for (var u = 0; u < $scope.totalConjuntos.length; u++) {
               if(conjuntos[i].name == $scope.totalConjuntos[u].name){
                    console.log(conjuntos[i])
                   if(!$scope.totalConjuntos[u].getStatus){
                       console.log("farso")
                       return false
                   }
               }

            }

        }
        return true
    }
    $scope.$watch('totalConjuntos', function() {
        console.log("watche")
        $scope.userTableinit()
    },true)
    $scope.respondedFilter= function(x) {
        if(!$scope.getResponded){
            return !x.responded
        }
        else{
            return true
        }
    }
    $scope.notRespondedFilter= function(x) {
        if(!$scope.getNotResponded){
            return x.responded
        }
        else{
            return true
        }
    }
    $scope.sendedFilter= function(x) {
        if(!$scope.getSended){
            return !x.enviada
        }
        else{
            return true
        }
    }
    $scope.notSendedFilter= function(x) {
        if(!$scope.getNotSended){
            return x.enviada
        }
        else{
            return true
        }
    }

    $scope.userTableinit = function() {
     $scope.usuarios = $scope.surveyDetails.usuarios.filter(function(usuario) {
       // Create an array using `.split()` method
         $scope.selected=[]
       return ($scope.conjuntosFilter(usuario) && $scope.respondedFilter(usuario) && $scope.notRespondedFilter(usuario) && $scope.sendedFilter(usuario) && $scope.notSendedFilter(usuario))

       // Filter the returned array based on specified filters
       // If the length of the returned filtered array is equal to
       // length of the filters array the element should be returned
       return cats.filter(function(cat) {
           return filtersArray.indexOf(cat) > -1;
       }).length === filtersArray.length;
    });
}
    $scope.userTableinit()

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
    $mdDialog.show({
      controller: DialogController,
      templateUrl: '/static/html/angular/info_encuesta.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:false,
      fullscreen: true // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
      $scope.status = 'You said the information was "' + answer + '".';
    }, function() {
      $scope.status = 'You cancelled the dialog.';
    });
  };
    $scope.getConjuntos= function(conjuntos) {
    var total =""
    for (var i = 0; i < conjuntos.length; i++) {
      var obj = conjuntos[i];
      total = total + " " + obj.name
    }
    return total
  }
});