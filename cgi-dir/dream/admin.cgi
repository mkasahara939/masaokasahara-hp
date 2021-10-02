#!/usr/bin/perl

#┌─────────────────────────────────
#│ DreamCounter : admin.cgi - 2011/09/27
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 設定ファイル取込
require './init.cgi';
my %cf = &init;

# データ受理
my %in = &parse_form;

# パスワード認証
&check_passwd;

# 処理分岐
if ($in{data_new}) { &data_new; }
if ($in{data_mente}) { &data_mente; }

# メニュー画面
&menu_html;

#-----------------------------------------------------------
#  メニュー画面
#-----------------------------------------------------------
sub menu_html {
	&header("メニューTOP");

	print <<EOM;
<div align="center">
<p>選択ボタンを押してください。</p>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<table border="1" cellpadding="5" cellspacing="0">
<tr>
	<th bgcolor="#cccccc">選択</th>
	<th bgcolor="#cccccc" width="250">処理メニュー</th>
</tr><tr>
	<th><input type="submit" name="data_new" value="選択"></th>
	<td>ログID新規作成</td>
</tr><tr>
	<th><input type="submit" name="data_mente" value="選択"></th>
	<td>ログIDメンテナンス（修正・削除）</td>
</tr><tr>
	<th><input type="button" value="選択" onclick="javascript:window.location='$cf{admin_cgi}'"></th>
	<td>ログアウト</td>
</tr>
</table>
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  新規記事作成
#-----------------------------------------------------------
sub data_new {
	my $log = shift;
	if ($log =~ /^(\d+):/) { $log = $1; }

	# 新規記事追加
	if ($in{job} eq "new") {
		&data_add;
	}

	# パラメータ指定
	my ($mode,$job);
	if ($in{data_new}) {
		$mode = "data_new";
		$job = "new";
		$log = 0;
	} else {
		$mode = "data_mente";
		$job = "edit2";
	}

	&header("メニューTOP ＞ 新規ID作成");
	&back_btn;
	print <<EOM;
<b class="ttl">■ID作成フォーム</b>
<hr color="#00f078">
<p>必要項目を入力して、送信ボタンを押してください。</p>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="$mode" value="1">
<input type="hidden" name="job" value="$job">
<table border="1" cellpadding="4" cellspacing="0">
<tr>
	<th bgcolor="#cccccc" nowrap>ID名</th>
	<td>
EOM

	if ($job eq 'new') {
		print qq|<input type="text" name="id" size="12" value="$in{id}">\n|;
		print qq|（半角英・数字、アンダーバーのみ）\n|;
	} else {
		print "<b>$in{id}</b>\n";
		print qq|<input type="hidden" name="id" value="$in{id}">\n|;
	}

	print <<EOM;
	</td>
</tr><tr>
	<th bgcolor="#cccccc" nowrap>開始番号</th>
	<td><input type="text" name="start" size="12" value="$log"></td>
</tr>
</table>
<br>
<input type="submit" value="送信する">
</form>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  データ追加
#-----------------------------------------------------------
sub data_add {
	# チェック
	if ($in{id} eq "") {
		&error("ID名が未入力です");
	}
	if ($in{id} =~ /\W/) {
		&error("ID名は半角英数字、アンダーバーのみです");
	}
	if (-e "$cf{datadir}/$in{id}.dat") {
		&error("指定したID名は既に使用されています");
	}
	$in{start} =~ s/\D//g;

	# 作成
	open(DAT,"+> $cf{datadir}/$in{id}.dat") || &error("write err: $in{id}.dat");
	print DAT $in{start};
	close(DAT);

	# 完了メッセージ
	&message("新規IDを追加しました", 'data_new');
}

#-----------------------------------------------------------
#  記事メンテナンス
#-----------------------------------------------------------
sub data_mente {
	# 指示フラグ
	my $job = $in{job};

	# 修正フォーム
	if ($job eq "edit" && $in{id} ne '') {

		open(IN,"$cf{datadir}/$in{id}.dat") || &error("open err: $in{id}.dat");
		my $data = <IN>;
		close(IN);

		# 修正フォーム
		&data_new($data);

	# 修正実行
	} elsif ($job eq "edit2") {

		open(DAT,"+> $cf{datadir}/$in{id}.dat") || &error("wrire err: $in{id}.dat");
		eval "flock(DAT, 2);";
		print DAT $in{start};
		close(DAT);

		# 完了メッセージ
		&message("修正を完了しました", 'data_mente');

	# 削除
	} elsif ($job eq "dele" && $in{id} ne "") {

		unlink("$cf{datadir}/$in{id}.dat");
	}

	&header("メニューTOP ＞ IDログメンテナンス");
	&back_btn;
	print <<EOM;
<b class="ttl">■IDログメンテナンス</b>
<hr color="#00f078">
<p>処理を選択し、送信ボタンを押してください。</p>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="data_mente" value="1">
処理：
<select name="job">
<option value="edit">修正
<option value="dele">削除
</select>
<input type="submit" value="送信">
<p></p>
<table border="1" cellpadding="2" cellspacing="0">
<tr>
	<th bgcolor="#cccccc" nowrap>選択</th>
	<th bgcolor="#cccccc" nowrap>IDログ</th>
</tr>
EOM

	opendir(DIR,"$cf{datadir}");
	while( defined( $_ = readdir(DIR) ) ) {
		next if (!/^(\w+)\.dat$/);

		print qq|<tr><th><input type="radio" name="id" value="$1"></th>|;
		print qq|<td>$1</td></tr>\n|;
	}
	closedir(DIR);

	print <<EOM;
</table>
</form>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  フォームデコード
#-----------------------------------------------------------
sub parse_form {
	my ($buf,%in);
	if ($ENV{REQUEST_METHOD} eq "POST") {
		&error('受理できません') if ($ENV{CONTENT_LENGTH} > $cf{maxdata});
		read(STDIN, $buf, $ENV{CONTENT_LENGTH});
	} else {
		$buf = $ENV{QUERY_STRING};
	}
	foreach ( split(/&/, $buf) ) {
		my ($key,$val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# 無効化
		$val =~ s/["'<>&\r\n]//g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	return %in;
}

#-----------------------------------------------------------
#  パスワード認証
#-----------------------------------------------------------
sub check_passwd {
	# パスワードが未入力の場合は入力フォーム画面
	if ($in{pass} eq "") {
		&enter_form;

	# パスワード認証
	} elsif ($in{pass} ne $cf{password}) {
		&error("認証できません");
	}
}

#-----------------------------------------------------------
#  入室画面
#-----------------------------------------------------------
sub enter_form {
	&header("入室画面");
	print <<EOM;
<div style="margin-top:4em;text-align:center;">
<form action="$cf{admin_cgi}" method="post">
<table width="380">
<tr>
	<td height="40" align="center">
		<fieldset><legend>管理パスワード入力</legend>
		<br>
		<input type="password" name="pass" value="" size="20">
		<input type="submit" value=" 認証 ">
		<br><br>
		</fieldset>
	</td>
</tr>
</table>
</form>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  エラー処理
#-------------------------------------------------
sub error {
	my $err = shift;

	&header;
	print <<EOM;
<div align="center">
<h3>ERROR !</h3>
<font color="red">$err</font>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  HTMLヘッダー
#-------------------------------------------------
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body,th,td { font-size:80%; }
.ttl { color: #004040; }
.eng { font-family:Verdana,Helvetica,Arial; }
-->
</style>
<title>夢カウンタ</title>
</head>
<body>
EOM
}

#-----------------------------------------------------------
#  戻りボタン
#-----------------------------------------------------------
sub back_btn {
	print <<EOM;
<div align="right">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="&lt; メニュー">
</form>
</div>
EOM
}

#-----------------------------------------------------------
#  メッセージ表示
#-----------------------------------------------------------
sub message {
	my ($msg, $param) = @_;

	&header("処理完了");
	print <<EOM;
<span style="color:#008000">$msg</span>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="$param" value="1">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="当初のフォームに戻る" style="width:160px">
</form>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="管理メニューに戻る" style="width:160px">
</form>
</body>
</html>
EOM
	exit;
}

