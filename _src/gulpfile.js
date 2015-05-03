'use strict';

var gulp = require('gulp');
var changed = require('gulp-changed');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');
var filter = require('gulp-filter');
var sass = require('gulp-sass');
var jade = require('gulp-jade');
var bs = require('browser-sync').create();


// configuration
var TEMPLATE_ROOT = '../_templates';
var SASS_APP = './sass/app.scss';
var CSS_DEST = TEMPLATE_ROOT + '/static/css';
var CSS_SOURCEMAP_REL_DEST = undefined;  // inline
var JADE_SRC = './views/*.tpl.jade';
var TEMPLATE_DEST = TEMPLATE_ROOT;
var SASS_WATCH = './sass/**/*.scss';
var JADE_WATCH = './views/**/*.jade';
var ENABLE_CACHEBUSTER = false;


var getStaticCachebuster = function() {
  return ENABLE_CACHEBUSTER ? '?_ts=' + (+new Date()).toString(36) : '';
};


gulp.task('sass', function() {
  var sassOptions = {
    outputStyle: 'compressed'
  };

  gulp.src(SASS_APP)
    .pipe(changed(CSS_DEST))
    .pipe(sourcemaps.init())
      .pipe(sass(sassOptions))
    .pipe(sourcemaps.write(CSS_SOURCEMAP_REL_DEST))
    .pipe(gulp.dest(CSS_DEST))
    .pipe(filter('**/*.css'))
    .pipe(bs.reload({ stream: true }))
    ;
});


gulp.task('jade', function() {
  var jadeLocals;
  jadeLocals = {
    STATIC_CACHEBUSTER_QS: getStaticCachebuster()
  };

  var jadeOptions = {
    pretty: true,
    locals: jadeLocals
  };

  return gulp.src(JADE_SRC)
    .pipe(changed(TEMPLATE_DEST))
    .pipe(jade(jadeOptions))
    .pipe(rename(function(path) {
      path.basename = path.basename.replace('.tpl', '');
    }))
    .pipe(gulp.dest(TEMPLATE_DEST))
    ;
});


gulp.task('jade-watch', ['jade'], function() {
  bs.reload();
});


gulp.task('serve', ['sass', 'jade'], function() {
  bs.init({
    server: {
      baseDir: TEMPLATE_DEST
    }
  });

  gulp.watch(SASS_WATCH, ['sass']);
  gulp.watch(JADE_WATCH, ['jade-watch']);
});


gulp.task('default', ['sass', 'jade']);


// vim:set ai et ts=2 sw=2 sts=2 fenc=utf-8:
