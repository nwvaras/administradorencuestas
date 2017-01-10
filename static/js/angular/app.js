'use strict';

angular.module('DiscusionAbiertaApp',['ngMaterial', 'ngMessages','material.svgAssetsCache','nvd3','md.data.table','ngMdIcons'])
  .config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  })
  .config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  })
.config(function($mdIconProvider) {
  $mdIconProvider
    .iconSet('social', 'img/icons/sets/social-icons.svg', 24)
    .iconSet('device', 'img/icons/sets/device-icons.svg', 24)
    .iconSet('communication', 'img/icons/sets/communication-icons.svg', 24)
    .defaultIconSet('img/icons/sets/core-icons.svg', 24);
})
.directive('mdtCustomCellCheckbox', function () {
  return {
    template: '<md-checkbox aria-label="Editar" class="md-secondary"></md-checkbox>',
  };
});;
