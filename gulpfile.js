var gulp = require('gulp');

var sass_dest = "app/static/styles/css";

// Compiles .sass into .css
gulp.task('sass', function() {
	var sass = require('gulp-sass');

	gulp.src('app/static/styles/sass/*.sass')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest(sass_dest));
});

// Monitors and .sass
gulp.task('watch', function() {
	gulp.watch('app/static/styles/sass/**/*', ['sass']);
});

//
gulp.task('default', ['watch']);
