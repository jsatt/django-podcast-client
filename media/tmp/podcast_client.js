(function() {
  angular.module('podcastClient.directives', []).directive('backBtn', function() {
    return {
      restrict: 'E',
      replace: true,
      controller: [
        '$scope', function($scope) {
          return $scope.go_back = function() {
            return history.back();
          };
        }
      ],
      template: '<div ng-if="$state.current.name != \'podcast-client.channels\'" ><a ng-click="go_back()"><i class="glyphicon glyphicon-chevron-left"></i>Back</a></div>'
    };
  }).directive('listened', function() {
    return {
      restrict: 'E',
      replace: true,
      template: '<span ng-switch="item.listened">\n    <i class="glyphicon glyphicon-star" ng-switch-when="true" title="Listened"></i>\n    <i class="glyphicon glyphicon-star-empty" ng-switch-when="false" title="Not Listened"></i>\n</span>'
    };
  }).directive('mediaType', function() {
    return {
      restrict: 'E',
      replace: true,
      template: '<span ng-switch="item.media_type">\n    <i class="glyphicon glyphicon-film" ng-switch-when="video" title="Video"></i>\n    <i class="glyphicon glyphicon-headphones" ng-switch-when="audio" title="Audio"></i>\n    <i class="glyphicon glyphicon-file" ng-switch-when="unknown" title="Unknown Media Type"></i>\n</span>'
    };
  }).directive('externalLink', function() {
    return {
      restrict: 'E',
      replace: true,
      scope: {
        url: '='
      },
      transclude: true,
      template: '<a ng-href="[[url]]" target="blank" class="external-link"><span ng-transclude></span> <i class="glyphicon glyphicon-new-window" title="External Link"></i></a>'
    };
  }).directive('downloadIndicator', function() {
    return {
      restrict: 'E',
      replace: true,
      template: '<span ng-switch="channel.download_new">\n    Download New:\n    <i class="glyphicon glyphicon-check" ng-switch-when="true" title="Download"></i>\n    <i class="glyphicon glyphicon-unchecked" ng-switch-when="false" title="Do Not Download"></i>\n</span>'
    };
  });

}).call(this);

(function() {
  var pcApp;

  pcApp = angular.module('pcApp', ['ui.router', 'podcastClient.directives', 'podcastClient.services']);

  pcApp.config([
    '$stateProvider', '$locationProvider', '$interpolateProvider', '$urlRouterProvider', function($stateProvider, $locationProvider, $interpolateProvider, $urlRouterProvider) {
      var getTemplate;
      $interpolateProvider.startSymbol('[[');
      $interpolateProvider.endSymbol(']]');
      getTemplate = function(name) {
        return function() {
          return document.getElementById(name).innerHTML;
        };
      };
      $locationProvider.html5Mode(true);
      return $stateProvider.state('podcast-client', {
        url: '/podcasts/',
        abstract: true,
        templateProvider: getTemplate('base.html')
      }).state('podcast-client.channels', {
        url: '',
        views: {
          content: {
            templateProvider: getTemplate('channel-list.html'),
            resolve: {
              channels: [
                'Channel', function(Channel) {
                  return Channel.query();
                }
              ]
            },
            controller: [
              '$scope', 'channels', function($scope, channels) {
                return $scope.channels = channels;
              }
            ]
          }
        }
      }).state('podcast-client.channel', {
        url: ':slug',
        resolve: {
          channel: [
            '$stateParams', 'Channel', function($stateParams, Channel) {
              return Channel.get({
                slug: $stateParams.slug
              });
            }
          ]
        },
        views: {
          content: {
            templateProvider: getTemplate('channel-details.html'),
            controller: [
              '$scope', 'channel', function($scope, channel) {
                return $scope.channel = channel;
              }
            ]
          },
          sidebar: {
            templateProvider: getTemplate('channel-details-sidebar.html'),
            controller: [
              '$scope', 'channel', function($scope, channel) {
                return $scope.channel = channel;
              }
            ]
          }
        },
        controller: [
          '$scope', function($scope) {
            return $scope.prev_view = 'podcast-client.channels';
          }
        ]
      }).state('podcast-client.item', {
        url: 'items/:slug',
        resolve: {
          item: [
            '$stateParams', 'Item', function($stateParams, Item) {
              return Item.get({
                slug: $stateParams.slug
              });
            }
          ]
        },
        views: {
          content: {
            templateProvider: getTemplate('item-details.html'),
            controller: [
              '$scope', 'item', function($scope, item) {
                return $scope.item = item;
              }
            ]
          },
          sidebar: {
            templateProvider: getTemplate('item-details-sidebar.html'),
            controller: [
              '$scope', 'item', function($scope, item) {
                return $scope.item = item;
              }
            ]
          }
        }
      });
    }
  ]);

  angular.module("pcApp").run([
    '$rootScope', '$state', '$stateParams', function($rootScope, $state, $stateParams) {
      $rootScope.$state = $state;
      return $rootScope.$stateParams = $stateParams;
    }
  ]);

}).call(this);

(function() {
  angular.module('podcastClient.services', ['ngResource']).factory('Channel', [
    '$resource', function($resource) {
      return $resource('/podcasts/api/channels/:slug');
    }
  ]).factory('Item', [
    '$resource', function($resource) {
      return $resource('/podcasts/api/items/:slug');
    }
  ]);

}).call(this);
