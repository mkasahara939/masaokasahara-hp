#!/usr/bin/perl

#��������������������������������������������������������������������
#�� DreamCounter : dream.cgi - 2011/06/09
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# ���W���[���錾
use strict;

# �ݒ�t�@�C���捞
require './init.cgi';
my %cf = &init;

# �f�[�^��
my %in = &parse_form;

# ���T�C�g����̃A�N�Z�X�r��
if ($cf{base_url}) {
	my $ref = $ENV{HTTP_REFERER};
	$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if ($ref && $ref !~ /$cf{base_url}/i) { &error; }
}

# �摜�f�B���N�g�����`
if ($in{gif}) {
	$cf{gifdir} =~ s|(.*)\d+$|$1$in{gif}|g;
}

# --- �J�E���^����
if ($in{id} ne "") {

	&counter;

# --- ���ԏ���
} elsif ($in{mode} eq "time") {

	# ���Ԏ擾
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

	# �摜�\��
	&load_image($count);

# --- �J�����_����
} elsif ($in{mode} eq "date") {

	# ���Ԏ擾
	my ($min,$hour,$mday,$mon,$year) = &get_time;

	my $count;
	if ($in{year} == 4) {
		$count = $year . 'd' . $mon . 'd' . $mday;
	} else {
		$year = sprintf("%02d", $year-2000);
		$count = $year . 'd' . $mon . 'd' . $mday;
	}

	# �摜�\��
	&load_image($count);

# --- �X�V���ԕ\������
} elsif ($in{file}) {

	# �t�@�C�����Ȃ���΃G���[
	unless (-e $in{file}) { &error; }

	# �X�V�������擾
	my ($mtime) = (stat($in{file}))[9];

	# �X�V����
	my ($min,$hour,$mday,$mon,$year) = &get_time($mtime);

	# �X���b�V�� "/" ���Ȃ���΃_�b�V�� "-" �ő�p
	my $slush = "$cf{gifdir}/s.gif";
	my $s;
	if (-e $slush) { $s = 's'; } else { $s = 'd'; }

	# �摜�\��
	my $count = $year . $s . $mon . $s . $mday . 'd' . $hour . 'c' . $min;
	&load_image($count);

# --- �t�@�C���T�C�Y���\������
} elsif ($in{size}) {

	# �t�@�C�����Ȃ���΃G���[
	unless (-e $in{size}) { &error; }

	# �T�C�Y�����擾 (bytes)
	my ($size) = (stat($in{size}))[7];

	# �P�ʕϊ��i�l�̌ܓ��j
	if ($in{p} eq 'k') {
		$size = int(($size / 1024)+0.5);
	} elsif ($in{p} eq 'm') {
		$size = int(($size / 1048576)+0.5);
	}

	# �摜�\��
	&load_image($size);

# --- �����\���i�����̂݁j
} elsif ($in{num} ne "") {

	# �摜�\��
	&load_image($in{num});

# --- �����_�����[�h
} else {

	if ($in{fig} > $cf{maxfig}) { $in{fig} = $cf{maxfig}; }
	$in{fig} ||= 5;

	srand;
	my $count;
	foreach (1 .. $in{fig}) {
		$count .= int(rand(10));
	}

	# �摜�\��
	&load_image($count);
}

#-----------------------------------------------------------
#  GIF�o��
#-----------------------------------------------------------
sub load_image {
	my $count = shift;

	# Image::Magick�̂Ƃ�
	if ($cf{image_pm} == 1) {
		require $cf{magick_pl};
		&magick($count, $cf{gifdir});
	}

	# ���C�u������荞��
	require $cf{gifcat_pl};

	# �摜�p�X�擾
	my @image;
	foreach ( split(//, $count) ) {
		push(@image,"$cf{gifdir}/$_.gif");
	}

	# �A���\��
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat::gifcat(@image);
	exit;
}

#-----------------------------------------------------------
#  �J�E���^�X�V
#-----------------------------------------------------------
sub counter {
	# ���O���`
	my $logfile = "$cf{datadir}/$in{id}.dat";

	# ���O�̑��݂��`�F�b�N
	unless(-e $logfile) { &error; }

	# �������`
	if ($in{fig} > $cf{maxfig}) { $in{fig} = $cf{maxfig}; }
	$in{fig} ||= 5;


	# �L�^�t�@�C������ǂݍ���
	open(DAT,"+< $logfile") || &error;
	eval "flock(DAT, 2);";
	my $data = <DAT>;
	
	# �L�^�t�@�C���𕪉�
	my ($count, $ip) = split(/:/, $data);

	# IP�A�h���X���擾
	my $addr = $ENV{REMOTE_ADDR};

	# IP�`�F�b�Nbackup
	my $flg;
	if($cf{ip_chk} && $addr eq $ip) { $flg = 1; }

	# ���O�X�V
	if (!$flg) {
		# �J�E���g�A�b�v
		$count++;

		# �t�@�C�����t�H�[�}�b�g
		if ($cf{ip_chk}) {
			$data = "$count:$addr";
		} else {
			$data = $count;
		}

		# �L�^�t�@�C���X�V
		seek(DAT, 0, 0);
		print DAT $data;
		truncate(DAT, tell(DAT));
	}
	close(DAT);

	# ��������
	while ( length($count) < $in{fig} ) {
		$count = '0' . $count;
	}

	# �摜�\��
	&load_image($count);
}

#-----------------------------------------------------------
#  �t�H�[���f�R�[�h
#-----------------------------------------------------------
sub parse_form {
	my $buf = $ENV{QUERY_STRING};

	my %in;
	foreach ( split(/&/, $buf) ) {
		my ($key, $val) = split(/=/);

		$in{$key} = $val;
	}

	# ���Q��
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
#  ���Ԏ擾
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
#  �G���[����
#-----------------------------------------------------------
sub error {
	# �G���[�摜
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

