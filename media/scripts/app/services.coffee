
angular.module('podcastClient.services', ['ngResource'])
.factory('Channel', ['$resource', ($resource) ->
    $resource '/podcasts/api/channels/:slug'
])
.factory('Item', ['$resource', ($resource) ->
    $resource '/podcasts/api/items/:slug'
])
