var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');

const SRC_DIR = './src/style';
const DEST_DIR = './assets/style';

// SassとCSSの保存先を指定
gulp.task('sass', function(){
  gulp.src(`${SRC_DIR}/**/*.scss`)
    .pipe(sass({outputStyle: 'expanded'}))
    .pipe(gulp.dest(DEST_DIR));
});

// CSSにベンダープレフィックスを付与
gulp.task('autoprefixer', () =>
    gulp.src(`${DEST_DIR}/**/*.css`)
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        .pipe(gulp.dest(DEST_DIR))
);

//自動監視のタスクを作成(sass-watchと名付ける)
gulp.task('sass-watch', ['sass'], function() {
  var watcher = gulp.watch(`${SRC_DIR}/**/*.scss`, ['sass']);
  watcher.on('change', function(event) {
  });
});

// タスク"task-watch"がgulpと入力しただけでdefaultで実行されるようになる
gulp.task('default', ['sass-watch']);
