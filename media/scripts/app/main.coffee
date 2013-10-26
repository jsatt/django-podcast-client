pcApp = angular.module('pcApp', ['ui.router', 'podcastClient.directives', 'podcastClient.services'])

pcApp.config ['$stateProvider', '$locationProvider', '$interpolateProvider', '$urlRouterProvider', ($stateProvider, $locationProvider, $interpolateProvider, $urlRouterProvider) ->
    $interpolateProvider.startSymbol('[[')
    $interpolateProvider.endSymbol(']]')

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
        url: ''
        views:
            content:
                templateProvider: getTemplate('channel-list.html')
                resolve:
                    channels: ['Channel', (Channel) ->
                        Channel.query()
                    ]
                controller: ['$scope', 'channels', ($scope, channels) ->
                    $scope.channels = channels
                ]
    .state 'podcast-client.channel',
        url: ':slug'
        resolve:
            channel: ['$stateParams', 'Channel', ($stateParams, Channel) ->
                Channel.get({slug: $stateParams.slug})
            ]
        views:
            content:
                templateProvider: getTemplate('channel-details.html')
                controller: ['$scope', 'channel', ($scope, channel) ->
                    $scope.channel = channel
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
