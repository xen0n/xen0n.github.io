'use strict';

var gulp = require('gulp');
var changed = require('gulp-changed');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');
var sass = require('gulp-sass');
var jade = require('gulp-jade');


// configuration
var SASS_APP = './sass/app.scss';
var CSS_DEST = '../static/css';
var CSS_SOURCEMAP_REL_DEST = '_sourcemap';
var JADE_SRC = './views/*.tpl.jade';
var TEMPLATE_DEST = '../_templates';


var getStaticCachebuster = function() {
  return (+new Date()).toString(36);
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
    .pipe(gulp.dest(CSS_DEST));
});


gulp.task('jade', function() {
  var jadeLocals = {
    STATIC_CACHEBUSTER_QS: '_ts=' + getStaticCachebuster()
  };

  var jadeOptions = {
    pretty: true,
    locals: jadeLocals
  };

  gulp.src(JADE_SRC)
    .pipe(changed(TEMPLATE_DEST))
    .pipe(jade(jadeOptions))
    .pipe(rename(function(path) {
      path.basename = path.basename.replace('.tpl', '');
    }))
    .pipe(gulp.dest(TEMPLATE_DEST));
});


gulp.task('default', ['sass', 'jade']);


// vim:set ai et ts=2 sw=2 sts=2 fenc=utf-8:
