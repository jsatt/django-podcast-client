module.exports = (grunt) ->
    grunt.initConfig
        pkg: grunt.file.readJSON 'package.json'
        stylus:
            compile:
                files:
                    'tmp/podcast_client.css': 'stylesheets/**/*.styl'
        coffee:
            compile:
                files:
                    'tmp/podcast_client.js': 'scripts/**/*.coffee'
        concat:
            scripts:
                files:
                    '../podcast_client/static/js/podcast_client.js': [
                        'scripts/vendor/jquery-2.0.3.min.js'
                        'scripts/vendor/angular.min.js'
                        'scripts/vendor/bootstrap.min.js'
                        'scripts/vendor/angular-resource.min.js'
                        'scripts/vendor/angular-route.min.js'
                        'scripts/vendor/angular-ui-router.min.js'
                        'tmp/podcast_client.js'
                    ]
            styles:
                files:
                    '../podcast_client/static/css/podcast_client.css': [
                        'stylesheets/vendor/bootstrap.min.css',
                        'stylesheets/vendor/bootstrap-responsive.min.css',
                        'tmp/podcast_client.css']
        watch:
            coffee:
                files: 'scripts/**/*.coffee'
                tasks: ['coffee', 'concat:scripts']
            js:
                files: 'scripts/**/*.js'
                tasks: ['concat:scripts']
            stylus:
                files: 'stylesheets/**/*.styl'
                tasks: ['stylus', 'concat:styles']
            css:
                files: 'stylesheets/**/*.css'
                tasks: ['concat:styles']

    grunt.loadNpmTasks 'grunt-contrib-concat'
    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-stylus'
    grunt.loadNpmTasks 'grunt-contrib-watch'

    grunt.registerTask 'default', ['stylus', 'coffee', 'concat']
    grunt.registerTask 'w', ['default', 'watch']
