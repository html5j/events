<?php

// ランダム文字列生成ツール
// http://www.itm-asp.com/randam/index.php

function h($str, $flag=true) {
	if ($flag) {
		return htmlspecialchars($str);
	} else {
		return $str;
	}
}


require_once '/home/sp/lib/CYUtilsLog.inc.php';
require_once '/home/sp/lib/CYUtilsDatabase.inc.php';

//$uri_root_dir = dirname($_SERVER['REQUEST_URI']);
$uri_root_tmp = explode('/', dirname($_SERVER['REQUEST_URI']));
$uri_root_dir = '/' . $uri_root_tmp[1];

/*
// Error
$error_num = 0;
$ERROR_MESSAGE[1] = 'IDが正しくありません。';
$ERROR_MESSAGE[2] = 'アンケートが登録されていません。';
$ERROR_MESSAGE[3] = '回答選択肢が登録されていません。';
$ERROR_MESSAGE[4] = '回答選択肢が正しく登録されていません。';
$ERROR_MESSAGE[5] = 'トランザクションに失敗しました。';
$ERROR_MESSAGE[6] = '登録に失敗しました。';
$ERROR_MESSAGE[7] = '回答が0件です。';
$ERROR_MESSAGE[8] = '不正なアクセスです。';

define('MAX_QUESTIONS', 30);		// 最大質問数
*/
define('PATH_INFO_DELIMITER', '/');	// PATH_INFO デリミタ
define('PATH_INFO_ELEMENTS', 4);	// PATH_INFO 構成要素数 (最大)
/*
define('MULTI_ANSWER_DELIMITER', ',');	// 複数回答 デリミタ

define('TEMPLATE_PATH_HEAD', './template/head/');
define('TEMPLATE_PATH_THX',  './template/thx/');
define('TEMPLATE_PATH_ANS',  './template/ans/');
define('TEMPLATE_PATH_ANS',  './template/ls/');

define('TEMPLATE_EXT_HEAD', '.head.tpl.php');
define('TEMPLATE_EXT_THX',  '.thx.tpl.php');
define('TEMPLATE_EXT_ANS',  '.ans.tpl.php');
define('TEMPLATE_EXT_ANS',  '.ls.tpl.php');
*/
$PATH_INFO       = $_SERVER['PATH_INFO'];
$PATH_INFO_ARRAY = explode(PATH_INFO_DELIMITER, $PATH_INFO, PATH_INFO_ELEMENTS);

$exec_type = '';
if (isset($PATH_INFO_ARRAY[2]) === true) {
	$exec_type = $PATH_INFO_ARRAY[2];
}

$exec_opt = '';
if (isset($PATH_INFO_ARRAY[3]) === true) {
	$exec_opt = $PATH_INFO_ARRAY[3];
}

$program_id = $PATH_INFO_ARRAY[1];

// ToDo
//if (strlen($program_id) <= 0) {
if ($program_id != 'abc' && $program_id != 'def' && $program_id != 'owcn' && $program_id != 'ent') {
	print 'program_id error.';
	exit;
}

/*
$con = dbConnect();

if (strlen($program_id) > 0) {

	$sql_where = ' where program_id = ' . getSqlValue($program_id);

	$sql = 'select keyword, program_text, submit_text from program_mst' . $sql_where;
	$res = dbQuery($con, $sql);

	$res_array = array();
	$rows = getNumRows($res, $res_array);

	if ($rows > 0) {
		$row = dbFetchRow($res, 0, $res_array);
		$keyword      = $row['keyword'];
		$program_text = $row['program_text'];
		$submit_text  = $row['submit_text'];
	} else {
		$error_num = 1;
	}
	dbFreeResult($res);

} else {
	$error_num = 1;
}
*/

$program_dir = $LOG_PATH . $uri_root_dir . '/' . $program_id;

function get_current_qn() {

	global $program_dir;

	$questions = glob($program_dir . '/*');

	if (count($questions) <= 0) {
		return false;
	}

	natsort($questions);
	$questions = array_merge($questions);

	$qn_dir = $questions[count($questions) - 1];
	list($qn, $mt_start, $an) = explode('#', $qn_dir, 3);

	$qn = basename($qn);

	return array($qn, $qn_dir);
}

function get_user_correct($qn, $mail) {

	global $program_dir;

    $command = 'ls -1d ' . $program_dir . '/' . $qn . '#*';
    exec($command, $res);

    if ($res) {
		$bqn_dir = $res[0];
		list($bqn, $mt_start, $ban) = explode('#', $bqn_dir, 3);
		
		$command2 = 'ls -1 ' . $bqn_dir . '/' . $ban . '#* | cut -d \'#\' -f 4,5 | sort';
		exec($command2, $res2);

    	if ($res2) {
    		$match = preg_grep('/' . $mail . '/', $res2);
    		if ($match) {
    			if (key($match) != (count($res2) - 1)) {
	    			return true;
    			}
    		}
		}
	}
	return false;
}

function get_an($qn, $qn_dir) {

	global $mail, $answer;

	// 1問目以外の時は、前問に正解しているか && 解答スピードが最下位ではないか をチェック
	// 途中で参加資格を復活させる場合は、復活する問題を以下のif条件に加える (ToDo: 全体的に処理をスマートに)
    if ($qn != 1 && $qn != 2 && $qn != 9 && $qn != 10)  {
		// 前問に正解していない or 解答スピードが最下位 の場合はエラーを返す
		if (!get_user_correct($qn - 1, $mail)) {
			return -1;
		}
	}

	$an_files = glob($qn_dir . '/*#' . $mail);

    // 解答送信済
	if (count($an_files) > 0) {
		$an_file =  basename($an_files[0]);
		list($an, $mt_submit, $tmp) = explode('#', $an_file, 3);
		$an = basename($an);

	// 初解答
	} else {

		// 既に解答を締め切っている場合はエラーを返す
		if (is_file($qn_dir . '/stop')) {
			return -2;
		}

		$filename[] = $answer;
		$filename[] = microtime(true);
		$filename[] = $mail;
		touch($qn_dir . '/' . implode('#', $filename));
		$an = 0;
	}

	return $an;
}

function get_qn_dir($qn) {

	global $program_dir;

	//$questions = glob($program_dir . '/' . $qn . '#*');
    $command = 'ls -1d ' . $program_dir . '/' . $qn . '#*';
    exec($command, $res);

    if ($res) {
		return $res[0];
    } else {
		return false;
    }
}

?>
