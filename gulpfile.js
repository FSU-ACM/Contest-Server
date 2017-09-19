var gulp = require('gulp');

var src = "app/static/styles/sass",
	dest = "app/static/styles/css";

// Compiles .sass into .css
gulp.task('sass', function() {
	var sass = require('gulp-sass');

	gulp.src(src)
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest(dest));
});

// Monitors and .sass
gulp.task('watch', function() {
	gulp.watch(src, ['sass']);
});

//
gulp.task('default', ['sass']);
