const gulp = require('gulp');
const sass = require('gulp-sass');


let src_old   = "app/static/styles/sass/*.sass",
	dest_old  = "app/static/styles/css",
	watch_old = "app/static/styles/sass/**";

// Compiles .sass into .css
gulp.task('sass', function () {
	return gulp.src("app/static/sass/*.sass")
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest("app/static/styles"));

});

gulp.task('sass_old', function() {

	return gulp.src(src_old)
			.pipe(sass().on('error', sass.logError))
			.pipe(gulp.dest(dest_old));

});

// Monitors and .sass
gulp.task('watch', ['sass'], function() {
	gulp.watch("app/static/sass/**/*.sass", ['sass']);
});

//
gulp.task('default', ['sass']);
