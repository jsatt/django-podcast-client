angular.module('podcastClient.directives', [])

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
    controller: ['$scope', '$timeout', '$window', 'Item', 'ItemFile', ($scope, $timeout, $window, Item, ItemFile) ->
        $scope.delete_file = ->
            if $window.confirm('Are you sure you want to delete this file from the server?')
                ItemFile.delete {slug: $scope.item.slug}, (resp) ->
                    $scope.item.file_downloaded = false

        $scope.download_file = ->
            $scope.fader()
            $scope.item.file_downloaded = 'downloading'
            ItemFile.download {slug: $scope.item.slug}, (resp) ->
                if resp.status == 'SUCCESS'
                    $scope.item.file_downloaded = true
                    $scope.cancel_fader()
                else
                    $scope.item.task_id = resp.task_id
                    $timeout($scope.check_download_status, 500)
            , (resp) ->
                $scope.item.file_downloaded = 'failed'
                $scope.cancel_fader()

        $scope.fader = ->
            $scope.element.toggleClass('out')
            $scope.item.fader_timeout = $timeout($scope.fader, 1000)

        $scope.cancel_fader = ->
            $timeout.cancel($scope.item.fader_timeout)
            $scope.element.removeClass('out')

        $scope.check_download_status = ->
            ItemFile.download_status {slug: $scope.item.slug, task_id: $scope.item.task_id}, (resp) ->
                if resp.status == 'SUCCESS'
                    $scope.cancel_fader()
                    Item.get {slug: $scope.item.slug}, (resp) ->
                        $scope.item = resp
                else if resp.status == 'FAILED'
                    $scope.item.file_downloaded = 'failed'
                    $scope.cancel_fader()
                else
                    $timeout($scope.check_download_status, 500)
            , (resp) ->
                $scope.item.file_downloaded = 'failed'
                $scope.cancel_fader()
    ]
    template: '''
        <span ng-switch="item.file_downloaded" class="downloaded_file">
            <i class="glyphicon glyphicon-saved" ng-switch-when="true" title="Delete from Server" ng-click="delete_file()"></i>
            <i class="glyphicon glyphicon-save" ng-switch-when="false" title="Retrieve to Server" ng-click="download_file()"></i>
            <i class="glyphicon glyphicon-import" ng-switch-when="downloading" title="Downloading"></i>
            <i class="glyphicon glyphicon-fire" ng-switch-when="failed" title="Failed to Download" ng-click="download_file()"></i>
        </span>'''
    link: (scope, element, attrs, ctrl) ->
        scope.element = element


.directive 'pagination', ->
    restrict: 'E'
    replace: true
    template: '''
        <ul class="pagination" ng-if="pages.length > 1">
            <li ng-if="current_page > 1"><a ui-sref=".({slug: $stateParams.slug, page: current_page - 1})">&laquo;</a></li>
            <li ng-repeat="page in pages" ng-class="{active: page == current_page || (page == 1 && !current_page)}"><a ui-sref=".({slug: $stateParams.slug, page: page})">[[page]]</a></li>
            <li ng-if="current_page < pages.length"><a ui-sref=".({slug: $stateParams.slug, page: current_page + 1})">&raquo;</a></li>
        </ul>'''
