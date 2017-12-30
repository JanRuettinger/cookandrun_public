'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var cleanCSS = require('gulp-clean-css');
var imagemin = require('gulp-imagemin');
var htmlmin = require('gulp-htmlmin');

var autoprefixer = require('gulp-autoprefixer');
var notify = require("gulp-notify");
var livereload = require('gulp-livereload');


// Compile Our Scss
gulp.task('sass', function() {
    return gulp.src('flask_app/static/sass/styles.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('flask_app/static/css/'))
        .pipe(notify({ message: 'sass to css conversion complete' }))
        .pipe(livereload());
});


// Minify CSS
gulp.task('minify-css', ['sass'] , function() {
  return gulp.src('flask_app/static/css/styles.css')
    .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
    .pipe(cleanCSS({compatibility: 'ie8'}))
    .pipe(rename('styles.min.css'))
    .pipe(notify({ message: 'css successfully minified' }))
    .pipe(gulp.dest('flask_app/static/css/'))
    .pipe(livereload());
});

// // Optimize images
// gulp.task('image-min', function() {
//   gulp.src(['flask_app/static/img/**/*.+(png|jpg|gif|svg)'])
//     .pipe(imagemin())
//     .pipe(gulp.dest('flask_app/static/img/opt'))
//     .pipe(notify({ message: 'image optimized successfully' }))
// });


// Watch Files For Changes
gulp.task('watch', function() {
    livereload.listen(1337);
    gulp.watch('flask_app/static/sass/**/*.scss', ['sass', 'minify-css']);
    gulp.watch('app/assets/img/**/*.+(png|jpg|gif|svg)',['image-min']);
});

// Default Task
gulp.task('default', ['sass', 'minify-css', 'watch']);

