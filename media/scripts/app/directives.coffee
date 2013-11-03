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
    controller: ['$scope', 'Item', ($scope, Item) ->
        $scope.toggle_listen = (listened) ->
            Item.update {slug: $scope.item.slug}, {listened: listened}, (resp) ->
                $scope.item = resp
    ]
    template: '''
        <span ng-switch="item.listened" class="listened">
            <i class="glyphicon glyphicon-ok yes" ng-switch-when="true" ng-click="toggle_listen(false)" title="Mark as New"></i>
            <i class="glyphicon glyphicon-star no" ng-switch-when="false" ng-click="toggle_listen(true)" title="Mark as Listened"></i>
        </span>'''

.directive 'mediaType', ->
    restrict: 'E'
    replace: true
    template: '''
        <span ng-switch="item.media_type" class="media_type">
            <i class="glyphicon glyphicon-film video" ng-switch-when="video" title="Video"></i>
            <i class="glyphicon glyphicon-headphones audio" ng-switch-when="audio" title="Audio"></i>
            <i class="glyphicon glyphicon-file unknown" ng-switch-when="unknown" title="Unknown Media Type"></i>
        </span>'''

.directive 'externalLink', ->
    restrict: 'E'
    replace: true
    scope:
        url: '='
    transclude: true
    template: '<a ng-href="[[url]]" target="blank" class="external-link"><span ng-transclude></span> <i class="glyphicon glyphicon-new-window" title="External Link"></i></a>'

.directive 'downloadNewIndicator', ->
    restrict: 'E'
    replace: true
    controller:['$scope', 'Channel', ($scope, Channel) ->
        $scope.toggle_download = (dl) ->
            Channel.update {slug: $scope.channel.slug} ,{download_new: dl}, (resp) ->
                $scope.channel = resp
    ]
    template: '''
        <span ng-switch="channel.download_new" class="download_new">
            Download New:
            <i class="glyphicon glyphicon-check" ng-switch-when="true" ng-click="toggle_download(false)" title="Download"></i>
            <i class="glyphicon glyphicon-unchecked" ng-switch-when="false" ng-click="toggle_download(true)" title="Do Not Download"></i>
        </span>'''

.directive 'downloadedFile', ->
    restrict: 'E'
    replace: true
    template: '''
        <span ng-switch="item.file_downloaded" class="downloaded_file">
            <i class="glyphicon glyphicon-saved" ng-switch-when="true" title="Delete from Server"></i>
            <i class="glyphicon glyphicon-save" ng-switch-when="false" title="Retrieve to Server"></i>
        </span>'''

.directive 'pagination', ->
    restrict: 'E'
    replace: true
    template: '''
        <ul class="pagination" ng-if="pages.length > 1">
            <li ng-if="current_page > 1"><a ui-sref="podcast-client.channel({slug: channel.slug, page: current_page - 1})">&laquo;</a></li>
            <li ng-repeat="page in pages" ng-class="{active: page == current_page || (page == 1 && !current_page)}"><a ui-sref="podcast-client.channel({slug: channel.slug, page: page})">[[page]]</a></li>
            <li ng-if="current_page < pages.length"><a ui-sref="podcast-client.channel({slug: channel.slug, page: current_page + 1})">&raquo;</a></li>
        </ul>'''
