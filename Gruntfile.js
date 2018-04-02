module.exports = function (grunt) {
    grunt.initConfig({
        watch: {
            files: ['www/static/sass/**/*.{scss,sass}'],
            tasks: ['sass']
        },

        sass: {
            dist: {
                files: {
                    'www/static/css/schedule.css': 'www/static/sass/manifest.scss',
                }
            }
        },

        browserSync: {
            dev: {
                bsFiles: {
                    src : [
                        'www/static/css/*.css',
                        'www/static/js/*.js',
                        '**/*.py',
                        '**/*.html'
                    ]
                },
                options: {
                    watchTask: true,
                    proxy: 'localhost:8000',
                    online: true,
                    open: false,
                    reloadDelay: 1500
                }
            }
        },

        shell: {
            djangoRun: {
                command: 'env/bin/python manage.py runserver',
                options: {
                  stdout: true,
                  failOnError: true,
                  async: true
                }
            },

            djangoRunWindows: {
                command: 'env\\Scripts\\python.exe manage.py runserver',
                options: {
                  stdout: true,
                  failOnError: true,
                  async: true
                }
            }
        }
    });

    // load npm tasks
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-browser-sync');
    grunt.loadNpmTasks('grunt-shell-spawn');

    // define default task
    grunt.registerTask('default', ['shell:djangoRun', 'browserSync', 'watch']);
    grunt.registerTask('windows', ['shell:djangoRunWindows', 'browserSync', 'watch']);
};
