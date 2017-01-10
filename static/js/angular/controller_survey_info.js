/**
 * Created by Nicolas on 01-01-2017.
 */
angular.module('DiscusionAbiertaApp').controller('MainCtrl', function($scope, $mdDialog,$http,$window,$mdToast){
    var last = {
      bottom: true,
      top:  false,
      left: false,
      right: true
    };

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

    $scope.surveyDetails = pre.surveyDetails

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
    var getMessages = function () {
    $http({
      method: 'POST',
      url: '/encuestas/mensajes/',
      data: { test: 'test' }
    }).then(function (response) {

          $scope.messages = response.data.mensajes;
        console.log(response)


    });

  };
    getMessages()
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

   function DialogController($scope, $mdDialog) {
    $scope.hide = function() {
      $mdDialog.hide();
    };

    $scope.cancel = function() {
      $mdDialog.cancel();
    };

    $scope.answer = function(answer) {
      $mdDialog.hide(answer);
    };
  }
    $scope.loadSurveyDetail = function(survey){
        $window.location.href = '/encuestas/surveys/info/' + survey.pk;
    }

    $scope.enviarEncuesta = function(ev) {
        if($scope.selected.length>0){
        var enc = $scope.surveyDetails.encuesta

    // Appending dialog to document.body to cover sidenav in docs app
    var confirm = $mdDialog.confirm()
          .title('Envio de encuesta: ' + enc.titulo)
          .textContent('La encuesta sera enviada a los usuarios seleccionados')
          .ariaLabel('Envio')
          .targetEvent(ev)
          .ok('Ok')
          .cancel('Cancel');

    $mdDialog.show(confirm).then(function() {
            $scope.sendSurveys()

    }, function() {
    });
        }
  };

    $scope.showDialogMessage= function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: '/static/html/angular/send_message_survey.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:false,
      fullscreen: true // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
      $scope.sendMessage(answer)
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
    $scope.sendSurveys= function () {

    $http({
      method: 'POST',
      url: '/encuestas/surveys/send/',
      data: { encuesta:$scope.surveyDetails.encuesta,
          usuarios: $scope.selected
                }
    }).then(function (response) {
            afterChange()
            $scope.sendToast('Encuesta ' + encuesta.titulo + ' enviada')


    });
  }
    $scope.sendMessage= function (msj) {

    $http({
      method: 'POST',
      url: '/encuestas/message/send/',
      data: { message:msj,
          users: $scope.selected
                }
    }).then(function (response) {
            afterChange()
            $scope.sendToast('Mensaje enviado')


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