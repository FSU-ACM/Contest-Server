var gulp = require('gulp');

var src = "app/static/styles/sass/*.sass",
	dest = "app/static/styles/css",
	watch = "app/static/styles/sass/**";

// Compiles .sass into .css
gulp.task('sass', function() {
	var sass = require('gulp-sass');

	gulp.src(src)
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest(dest));
});

// Monitors and .sass
gulp.task('watch', ['sass'], function() {
	gulp.watch(watch, ['sass']);
});

//
gulp.task('default', ['sass']);
