#!/usr/bin/perl

#��������������������������������������������������������������������
#�� DreamCounter : check.cgi - 2011/09/27
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# ���W���[���錾
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

# �f�[�^�f�B���N�g��
my $flg;
if (-d $cf{datadir}) {
	$flg = 1;
	print "<li>�f�[�^�f�B���N�g���̃p�X : OK\n";
	if (-r $cf{datadir} && -w $cf{datadir} && -x $cf{datadir}) {
		print "<li>�f�[�^�f�B���N�g���̃p�[�~�b�V���� : OK\n";
	} else {
		print "<li>�f�[�^�f�B���N�g���̃p�[�~�b�V���� : NG\n";
	}

	# ���O�t�@�C������
	opendir(DIR,"$cf{datadir}");
	while( defined( $_ = readdir(DIR) ) ) {
		next if (!/^(\w+)\.dat$/);

		if (-w "$cf{datadir}/$_" && -r "$cf{datadir}/$_") {
			print "<li>$_ ���O�p�[�~�b�V���� : OK\n";
		} else {
			print "<li>$_ ���O�p�[�~�b�V���� : NG\n";
		}
	}
	closedir(DIR);

} else {
	print "<li>�f�[�^�f�B���N�g���̃p�X : NG �� $cf{datadir}\n";
}

# ���T�C�g����̃A�N�Z�X����
print "<li>���T�C�g����̃A�N�Z�X�����F";
if ($cf{base_url}) {
	print "���� �� $cf{base_url}\n";
} else {
	print "�Ȃ�\n";
}

# �摜�f�B���N�g���̃p�X�m�F
if (-d $cf{gifdir}) {
	print "<li>$cf{gifdir} : �摜�f�B���N�g���p�X : OK\n";
} else {
	print "<li>$cf{gifdir} : �摜�f�B���N�g���p�X : NG\n";
}

# �摜�`�F�b�N
foreach ("0".."9", "a", "p", "c", "d") {
	if (-e "$cf{gifdir}/$_.gif") {
		print "<li>$_ : �摜OK \n";
	} else {
		print "<li>$_ : �摜NG\n";
	}
}

eval { require $cf{gifcat_pl}; };
if ($@) {
	print "<li>gifcat.pl�e�X�g: NG\n";
} else {
	print "<li>gifcat.pl�e�X�g: OK\n";

	# �摜�A��
	if ($cf{image_pm} == 0) {
		print "<li>�摜�A���e�X�g �� <img src=\"$cf{dream_cgi}?num=0123456789\">\n";
	}
}

eval { require Image::Magick; };
if ($@) {
	print "<li>Image::Magick�e�X�g : NG\n";
} else {
	print "<li>Image::Magick�e�X�g : OK\n";

	# �摜�A��
	if ($cf{image_pm} == 1) {
		print "<li>�摜�A���e�X�g �� <img src=\"$cf{dream_cgi}?num=0123456789\">\n";
	}
}

# ���쌠�\���F�폜���ϋ֎~
print <<EOM;
</ul>
<p style="font-size:10px;font-family:Verdana,Helvetica,Arial;margin-top:5em;text-align:center;">
- <a href="http://www.kent-web.com/">DreamCounter</a> -
</p>
</body>
</html>
EOM
exit;

