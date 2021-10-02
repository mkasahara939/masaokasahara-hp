#!/usr/bin/perl

#┌─────────────────────────────────
#│ DreamCounter : dream.cgi - 2011/06/09
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;

# 設定ファイル取込
require './init.cgi';
my %cf = &init;

# データ受理
my %in = &parse_form;

# 他サイトからのアクセス排除
if ($cf{base_url}) {
	my $ref = $ENV{HTTP_REFERER};
	$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if ($ref && $ref !~ /$cf{base_url}/i) { &error; }
}

# 画像ディレクトリを定義
if ($in{gif}) {
	$cf{gifdir} =~ s|(.*)\d+$|$1$in{gif}|g;
}

# --- カウンタ処理
if ($in{id} ne "") {

	&counter;

# --- 時間処理
} elsif ($in{mode} eq "time") {

	# 時間取得
	my ($min,$hour,$mday,$mon,$year) = &get_time;

	my $count;
	if ($in{type} == 24) {
		$count = $hour . 'c' . $min;
	} else {
		my $head;
		if ($hour >= 12) {
			$hour = sprintf("%02d", $hour-12);
			$head = 'p';
		} else {
			$head = 'a';
		}
		$count = $head . $hour . 'c' . $min;
	}

	# 画像表示
	&load_image($count);

# --- カレンダ処理
} elsif ($in{mode} eq "date") {

	# 時間取得
	my ($min,$hour,$mday,$mon,$year) = &get_time;

	my $count;
	if ($in{year} == 4) {
		$count = $year . 'd' . $mon . 'd' . $mday;
	} else {
		$year = sprintf("%02d", $year-2000);
		$count = $year . 'd' . $mon . 'd' . $mday;
	}

	# 画像表示
	&load_image($count);

# --- 更新時間表示処理
} elsif ($in{file}) {

	# ファイルがなければエラー
	unless (-e $in{file}) { &error; }

	# 更新日数を取得
	my ($mtime) = (stat($in{file}))[9];

	# 更新時間
	my ($min,$hour,$mday,$mon,$year) = &get_time($mtime);

	# スラッシュ "/" がなければダッシュ "-" で代用
	my $slush = "$cf{gifdir}/s.gif";
	my $s;
	if (-e $slush) { $s = 's'; } else { $s = 'd'; }

	# 画像表示
	my $count = $year . $s . $mon . $s . $mday . 'd' . $hour . 'c' . $min;
	&load_image($count);

# --- ファイルサイズ数表示処理
} elsif ($in{size}) {

	# ファイルがなければエラー
	unless (-e $in{size}) { &error; }

	# サイズ数を取得 (bytes)
	my ($size) = (stat($in{size}))[7];

	# 単位変換（四捨五入）
	if ($in{p} eq 'k') {
		$size = int(($size / 1024)+0.5);
	} elsif ($in{p} eq 'm') {
		$size = int(($size / 1048576)+0.5);
	}

	# 画像表示
	&load_image($size);

# --- 強制表示（数字のみ）
} elsif ($in{num} ne "") {

	# 画像表示
	&load_image($in{num});

# --- ランダムモード
} else {

	if ($in{fig} > $cf{maxfig}) { $in{fig} = $cf{maxfig}; }
	$in{fig} ||= 5;

	srand;
	my $count;
	foreach (1 .. $in{fig}) {
		$count .= int(rand(10));
	}

	# 画像表示
	&load_image($count);
}

#-----------------------------------------------------------
#  GIF出力
#-----------------------------------------------------------
sub load_image {
	my $count = shift;

	# Image::Magickのとき
	if ($cf{image_pm} == 1) {
		require $cf{magick_pl};
		&magick($count, $cf{gifdir});
	}

	# ライブラリ取り込み
	require $cf{gifcat_pl};

	# 画像パス取得
	my @image;
	foreach ( split(//, $count) ) {
		push(@image,"$cf{gifdir}/$_.gif");
	}

	# 連結表示
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat::gifcat(@image);
	exit;
}

#-----------------------------------------------------------
#  カウンタ更新
#-----------------------------------------------------------
sub counter {
	# ログを定義
	my $logfile = "$cf{datadir}/$in{id}.dat";

	# ログの存在をチェック
	unless(-e $logfile) { &error; }

	# 桁数を定義
	if ($in{fig} > $cf{maxfig}) { $in{fig} = $cf{maxfig}; }
	$in{fig} ||= 5;


	# 記録ファイルから読み込み
	open(DAT,"+< $logfile") || &error;
	eval "flock(DAT, 2);";
	my $data = <DAT>;
	
	# 記録ファイルを分解
	my ($count, $ip) = split(/:/, $data);

	# IPアドレスを取得
	my $addr = $ENV{REMOTE_ADDR};

	# IPチェックbackup
	my $flg;
	if($cf{ip_chk} && $addr eq $ip) { $flg = 1; }

	# ログ更新
	if (!$flg) {
		# カウントアップ
		$count++;

		# ファイルをフォーマット
		if ($cf{ip_chk}) {
			$data = "$count:$addr";
		} else {
			$data = $count;
		}

		# 記録ファイル更新
		seek(DAT, 0, 0);
		print DAT $data;
		truncate(DAT, tell(DAT));
	}
	close(DAT);

	# 桁数調整
	while ( length($count) < $in{fig} ) {
		$count = '0' . $count;
	}

	# 画像表示
	&load_image($count);
}

#-----------------------------------------------------------
#  フォームデコード
#-----------------------------------------------------------
sub parse_form {
	my $buf = $ENV{QUERY_STRING};

	my %in;
	foreach ( split(/&/, $buf) ) {
		my ($key, $val) = split(/=/);

		$in{$key} = $val;
	}

	# 無害化
	$in{id}   =~ s/\W//g;
	$in{fig}  =~ s/\D//g;
	$in{num}  =~ s/\D//g;
	$in{mode} =~ s/\W//g;
	$in{year} =~ s/\D//g;
	$in{type} =~ s/\D//g;
	$in{p}    =~ s/\W//g;
	$in{file} =~ s/[<>"'&+;()\0\r\n]//g;
	$in{size} =~ s/[<>"'&+;()\0\r\n]//g;

	return %in;
}

#-----------------------------------------------------------
#  時間取得
#-----------------------------------------------------------
sub get_time {
	my $time = shift;
	$time ||= time;

	$ENV{TZ} = "JST-9";
	my ($min,$hour,$mday,$mon,$year) = (localtime($time))[1..5];

	$year += 1900;
	$mon  = sprintf("%02d", $mon + 1);
	$hour = sprintf("%02d", $hour);
	$min  = sprintf("%02d", $min);
	$mday = sprintf("%02d", $mday);

	return ($min,$hour,$mday,$mon,$year);
}

#-----------------------------------------------------------
#  エラー処理
#-----------------------------------------------------------
sub error {
	# エラー画像
	my @err = qw{
		47 49 46 38 39 61 2d 00 0f 00 80 00 00 00 00 00 ff ff ff 2c
		00 00 00 00 2d 00 0f 00 00 02 49 8c 8f a9 cb ed 0f a3 9c 34
		81 7b 03 ce 7a 23 7c 6c 00 c4 19 5c 76 8e dd ca 96 8c 9b b6
		63 89 aa ee 22 ca 3a 3d db 6a 03 f3 74 40 ac 55 ee 11 dc f9
		42 bd 22 f0 a7 34 2d 63 4e 9c 87 c7 93 fe b2 95 ae f7 0b 0e
		8b c7 de 02	00 3b
	};

	print "Content-type: image/gif\n\n";
	foreach (@err) {
		print pack('C*', hex($_));
	}
	exit;
}

