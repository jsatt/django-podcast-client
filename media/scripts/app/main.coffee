pcApp = angular.module('pcApp', ['ui.router', 'podcastClient.directives', 'podcastClient.services'])

pcApp.config ['$stateProvider', '$locationProvider', '$interpolateProvider', '$urlRouterProvider', '$httpProvider', ($stateProvider, $locationProvider, $interpolateProvider, $urlRouterProvider, $httpProvider) ->
    $interpolateProvider.startSymbol('[[')
    $interpolateProvider.endSymbol(']]')
    $httpProvider.defaults.xsrfCookieName = "csrftoken"
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken"

    getTemplate = (name) ->
        return ->
            document.getElementById(name).innerHTML

    $locationProvider.html5Mode(true)
    #$urlRouterProvider.otherwise('/podcasts/')

    $stateProvider
    .state 'podcast-client',
        url: '/podcasts/'
        abstract: true
        templateProvider: getTemplate('base.html')
    .state 'podcast-client.channels',
        url: '?page'
        views:
            content:
                templateProvider: getTemplate('channel-list.html')
                resolve:
                    channels: ['Channel', (Channel) ->
                        Channel.get()
                    ]
                controller: ['$scope', 'channels', ($scope, channels) ->
                    $scope.channels = channels

                    $scope.pages = []
                    $scope.current_page = if $scope.$stateParams.page then parseInt($scope.$stateParams.page) else 1
                    $scope.$watch 'channels.results', () ->
                        if $scope.channels.results
                            total_channels = $scope.channels.count
                            item_count = $scope.channels.results.length
                            page_count = Math.ceil(total_channels / item_count)
                            $scope.pages = [1..page_count]
                    $scope.$on '$stateChangeStart', (event, toState, toParams, fromState, fromParams) ->
                        toParams.parentStateParams = fromParams
                ]
    .state 'podcast-client.channel',
        url: ':slug?page'
        resolve:
            channel: ['$stateParams', 'Channel', ($stateParams, Channel) ->
                Channel.get({slug: $stateParams.slug})
            ]
            items: ['$stateParams', 'Items', ($stateParams, Items) ->
                Items.get({slug: $stateParams.slug, page: $stateParams.page})
            ]
        views:
            content:
                templateProvider: getTemplate('channel-details.html')
                controller: ['$scope', 'channel', 'items', ($scope, channel, items) ->
                    $scope.items = items
                    $scope.channel = channel

                    $scope.pages = []
                    $scope.current_page = if $scope.$stateParams.page then parseInt($scope.$stateParams.page) else 1
                    $scope.$watch 'items.results', () ->
                        if $scope.items.results
                            total_items = $scope.items.count
                            item_count = $scope.items.results.length
                            page_count = Math.ceil(total_items / item_count)
                            $scope.pages = [1..page_count]
                    $scope.$on '$stateChangeStart', (event, toState, toParams, fromState, fromParams) ->
                        toParams.parentStateParams = fromParams

                ]
            sidebar:
                templateProvider: getTemplate('channel-details-sidebar.html')
                controller: ['$scope', 'channel', ($scope, channel) ->
                    $scope.channel = channel
                ]
        controller: ['$scope', ($scope) ->
            $scope.prev_view = 'podcast-client.channels'
        ]
    .state 'podcast-client.item',
        url: 'items/:slug'
        resolve:
            item: ['$stateParams', 'Item', ($stateParams, Item) ->
                Item.get({slug: $stateParams.slug})
            ]
        views:
            content:
                templateProvider: getTemplate('item-details.html')
                controller: ['$scope', 'item', ($scope, item) ->
                    $scope.item = item
                ]
            sidebar:
                templateProvider: getTemplate('item-details-sidebar.html')
                controller: ['$scope', 'item', ($scope, item) ->
                    $scope.item = item
                ]
]

angular.module("pcApp").run ['$rootScope', '$state', '$stateParams', ($rootScope, $state, $stateParams) ->
        $rootScope.$state = $state
        $rootScope.$stateParams = $stateParams
        
]
