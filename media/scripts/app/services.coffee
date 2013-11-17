
angular.module('podcastClient.services', ['ngResource'])
.factory('Channel', ['$resource', ($resource) ->
    $resource '/podcasts/api/channels/:slug', {slug: '@slug'},
        update: {method: 'PATCH'}
])
.factory('Items', ['$resource', ($resource) ->
    $resource '/podcasts/api/channels/:slug/items', {slug: '@slug'}
])
.factory('Item', ['$resource', ($resource) ->
    $resource '/podcasts/api/items/:slug', {slug: '@slug'},
        update: {method: 'PATCH'}
])
.factory('ItemFile', ['$resource', ($resource) ->
    $resource '/podcasts/api/items/:slug/file', {slug: '@slug'},
        download: {method: 'GET', params: {download_file: ''}}
        download_status: {method: 'GET', params: {download_status: ''}}
])
