var gulp = require('gulp'),
    gp_concat = require('gulp-concat'),
    gp_rename = require('gulp-rename'),
    gp_uglify = require('gulp-uglify'),
    watch = require('gulp-watch');

var destination_path = 'senate/static/enem/js/build',
    js_path = 'senate/static/senate/js/react-components/parliamentary_profile.js';

gulp.task('concat', function(){
    return gulp.src(js_path)
            .pipe(gp_concat('app.js'))
            .pipe(gulp.dest(destination_path))

});

gulp.task('minify', function(){
    return gulp.src(js_path)
            .pipe(gp_rename('app.min.js'))
            .pipe(gp_uglify())
            .pipe(gulp.dest(destination_path));
});

gulp.task('default', ['concat','minify'], function(){});

gulp.task('watch', function() {
    gulp.watch(js_path, ['concat']);
});