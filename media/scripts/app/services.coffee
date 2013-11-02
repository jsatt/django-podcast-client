
angular.module('podcastClient.services', ['ngResource'])
.factory('Channel', ['$resource', ($resource) ->
    $resource '/podcasts/api/channels/:slug', {slug: '@slug'},
        update: {method: 'PATCH'}
])
.factory('Item', ['$resource', ($resource) ->
    $resource '/podcasts/api/items/:slug', {slug: '@slug'},
        update: {method: 'PATCH'}
])
