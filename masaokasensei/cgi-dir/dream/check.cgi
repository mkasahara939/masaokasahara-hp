#!/usr/bin/perl

#┌─────────────────────────────────
#│ DreamCounter : check.cgi - 2011/09/27
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;

require "./init.cgi";
my %cf = &init;

print <<EOM;
Content-type: text/html

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
EOM

# データディレクトリ
my $flg;
if (-d $cf{datadir}) {
	$flg = 1;
	print "<li>データディレクトリのパス : OK\n";
	if (-r $cf{datadir} && -w $cf{datadir} && -x $cf{datadir}) {
		print "<li>データディレクトリのパーミッション : OK\n";
	} else {
		print "<li>データディレクトリのパーミッション : NG\n";
	}

	# ログファイル検索
	opendir(DIR,"$cf{datadir}");
	while( defined( $_ = readdir(DIR) ) ) {
		next if (!/^(\w+)\.dat$/);

		if (-w "$cf{datadir}/$_" && -r "$cf{datadir}/$_") {
			print "<li>$_ ログパーミッション : OK\n";
		} else {
			print "<li>$_ ログパーミッション : NG\n";
		}
	}
	closedir(DIR);

} else {
	print "<li>データディレクトリのパス : NG → $cf{datadir}\n";
}

# 他サイトからのアクセス制限
print "<li>他サイトからのアクセス制限：";
if ($cf{base_url}) {
	print "あり → $cf{base_url}\n";
} else {
	print "なし\n";
}

# 画像ディレクトリのパス確認
if (-d $cf{gifdir}) {
	print "<li>$cf{gifdir} : 画像ディレクトリパス : OK\n";
} else {
	print "<li>$cf{gifdir} : 画像ディレクトリパス : NG\n";
}

# 画像チェック
foreach ("0".."9", "a", "p", "c", "d") {
	if (-e "$cf{gifdir}/$_.gif") {
		print "<li>$_ : 画像OK \n";
	} else {
		print "<li>$_ : 画像NG\n";
	}
}

eval { require $cf{gifcat_pl}; };
if ($@) {
	print "<li>gifcat.plテスト: NG\n";
} else {
	print "<li>gifcat.plテスト: OK\n";

	# 画像連結
	if ($cf{image_pm} == 0) {
		print "<li>画像連結テスト → <img src=\"$cf{dream_cgi}?num=0123456789\">\n";
	}
}

eval { require Image::Magick; };
if ($@) {
	print "<li>Image::Magickテスト : NG\n";
} else {
	print "<li>Image::Magickテスト : OK\n";

	# 画像連結
	if ($cf{image_pm} == 1) {
		print "<li>画像連結テスト → <img src=\"$cf{dream_cgi}?num=0123456789\">\n";
	}
}

# 著作権表示：削除改変禁止
print <<EOM;
</ul>
<p style="font-size:10px;font-family:Verdana,Helvetica,Arial;margin-top:5em;text-align:center;">
- <a href="http://www.kent-web.com/">DreamCounter</a> -
</p>
</body>
</html>
EOM
exit;

