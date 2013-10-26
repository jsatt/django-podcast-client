angular.module('podcastClient.directives', [])

.directive 'backBtn', ->
    restrict: 'E'
    replace: true
    controller: ['$scope', ($scope) ->
        $scope.go_back = ->
            history.back()
    ]
    template: '''<div ng-if="$state.current.name != 'podcast-client.channels'" ><a ng-click="go_back()"><i class="glyphicon glyphicon-chevron-left"></i>Back</a></div>'''

.directive 'listened', ->
    restrict: 'E'
    replace: true
    template: '''
        <span ng-switch="item.listened">
            <i class="glyphicon glyphicon-star" ng-switch-when="true" title="Listened"></i>
            <i class="glyphicon glyphicon-star-empty" ng-switch-when="false" title="Not Listened"></i>
        </span>'''

.directive 'mediaType', ->
    restrict: 'E'
    replace: true
    template: '''
        <span ng-switch="item.media_type">
            <i class="glyphicon glyphicon-film" ng-switch-when="video" title="Video"></i>
            <i class="glyphicon glyphicon-headphones" ng-switch-when="audio" title="Audio"></i>
            <i class="glyphicon glyphicon-file" ng-switch-when="unknown" title="Unknown Media Type"></i>
        </span>'''

.directive 'externalLink', ->
    restrict: 'E'
    replace: true
    scope:
        url: '='
    transclude: true
    template: '<a ng-href="[[url]]" target="blank" class="external-link"><span ng-transclude></span> <i class="glyphicon glyphicon-new-window" title="External Link"></i></a>'

.directive 'downloadIndicator', ->
    restrict: 'E'
    replace: true
    template: '''
        <span ng-switch="channel.download_new">
            Download New:
            <i class="glyphicon glyphicon-check" ng-switch-when="true" title="Download"></i>
            <i class="glyphicon glyphicon-unchecked" ng-switch-when="false" title="Do Not Download"></i>
        </span>'''
