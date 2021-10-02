#!/usr/bin/perl

#��������������������������������������������������������������������
#�� DreamCounter : admin.cgi - 2011/09/27
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# ���W���[���錾
use strict;
use CGI::Carp qw(fatalsToBrowser);

# �ݒ�t�@�C���捞
require './init.cgi';
my %cf = &init;

# �f�[�^��
my %in = &parse_form;

# �p�X���[�h�F��
&check_passwd;

# ��������
if ($in{data_new}) { &data_new; }
if ($in{data_mente}) { &data_mente; }

# ���j���[���
&menu_html;

#-----------------------------------------------------------
#  ���j���[���
#-----------------------------------------------------------
sub menu_html {
	&header("���j���[TOP");

	print <<EOM;
<div align="center">
<p>�I���{�^���������Ă��������B</p>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<table border="1" cellpadding="5" cellspacing="0">
<tr>
	<th bgcolor="#cccccc">�I��</th>
	<th bgcolor="#cccccc" width="250">�������j���[</th>
</tr><tr>
	<th><input type="submit" name="data_new" value="�I��"></th>
	<td>���OID�V�K�쐬</td>
</tr><tr>
	<th><input type="submit" name="data_mente" value="�I��"></th>
	<td>���OID�����e�i���X�i�C���E�폜�j</td>
</tr><tr>
	<th><input type="button" value="�I��" onclick="javascript:window.location='$cf{admin_cgi}'"></th>
	<td>���O�A�E�g</td>
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
#  �V�K�L���쐬
#-----------------------------------------------------------
sub data_new {
	my $log = shift;
	if ($log =~ /^(\d+):/) { $log = $1; }

	# �V�K�L���ǉ�
	if ($in{job} eq "new") {
		&data_add;
	}

	# �p�����[�^�w��
	my ($mode,$job);
	if ($in{data_new}) {
		$mode = "data_new";
		$job = "new";
		$log = 0;
	} else {
		$mode = "data_mente";
		$job = "edit2";
	}

	&header("���j���[TOP �� �V�KID�쐬");
	&back_btn;
	print <<EOM;
<b class="ttl">��ID�쐬�t�H�[��</b>
<hr color="#00f078">
<p>�K�v���ڂ���͂��āA���M�{�^���������Ă��������B</p>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="$mode" value="1">
<input type="hidden" name="job" value="$job">
<table border="1" cellpadding="4" cellspacing="0">
<tr>
	<th bgcolor="#cccccc" nowrap>ID��</th>
	<td>
EOM

	if ($job eq 'new') {
		print qq|<input type="text" name="id" size="12" value="$in{id}">\n|;
		print qq|�i���p�p�E�����A�A���_�[�o�[�̂݁j\n|;
	} else {
		print "<b>$in{id}</b>\n";
		print qq|<input type="hidden" name="id" value="$in{id}">\n|;
	}

	print <<EOM;
	</td>
</tr><tr>
	<th bgcolor="#cccccc" nowrap>�J�n�ԍ�</th>
	<td><input type="text" name="start" size="12" value="$log"></td>
</tr>
</table>
<br>
<input type="submit" value="���M����">
</form>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  �f�[�^�ǉ�
#-----------------------------------------------------------
sub data_add {
	# �`�F�b�N
	if ($in{id} eq "") {
		&error("ID���������͂ł�");
	}
	if ($in{id} =~ /\W/) {
		&error("ID���͔��p�p�����A�A���_�[�o�[�݂̂ł�");
	}
	if (-e "$cf{datadir}/$in{id}.dat") {
		&error("�w�肵��ID���͊��Ɏg�p����Ă��܂�");
	}
	$in{start} =~ s/\D//g;

	# �쐬
	open(DAT,"+> $cf{datadir}/$in{id}.dat") || &error("write err: $in{id}.dat");
	print DAT $in{start};
	close(DAT);

	# �������b�Z�[�W
	&message("�V�KID��ǉ����܂���", 'data_new');
}

#-----------------------------------------------------------
#  �L�������e�i���X
#-----------------------------------------------------------
sub data_mente {
	# �w���t���O
	my $job = $in{job};

	# �C���t�H�[��
	if ($job eq "edit" && $in{id} ne '') {

		open(IN,"$cf{datadir}/$in{id}.dat") || &error("open err: $in{id}.dat");
		my $data = <IN>;
		close(IN);

		# �C���t�H�[��
		&data_new($data);

	# �C�����s
	} elsif ($job eq "edit2") {

		open(DAT,"+> $cf{datadir}/$in{id}.dat") || &error("wrire err: $in{id}.dat");
		eval "flock(DAT, 2);";
		print DAT $in{start};
		close(DAT);

		# �������b�Z�[�W
		&message("�C�����������܂���", 'data_mente');

	# �폜
	} elsif ($job eq "dele" && $in{id} ne "") {

		unlink("$cf{datadir}/$in{id}.dat");
	}

	&header("���j���[TOP �� ID���O�����e�i���X");
	&back_btn;
	print <<EOM;
<b class="ttl">��ID���O�����e�i���X</b>
<hr color="#00f078">
<p>������I�����A���M�{�^���������Ă��������B</p>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="hidden" name="data_mente" value="1">
�����F
<select name="job">
<option value="edit">�C��
<option value="dele">�폜
</select>
<input type="submit" value="���M">
<p></p>
<table border="1" cellpadding="2" cellspacing="0">
<tr>
	<th bgcolor="#cccccc" nowrap>�I��</th>
	<th bgcolor="#cccccc" nowrap>ID���O</th>
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
#  �t�H�[���f�R�[�h
#-----------------------------------------------------------
sub parse_form {
	my ($buf,%in);
	if ($ENV{REQUEST_METHOD} eq "POST") {
		&error('�󗝂ł��܂���') if ($ENV{CONTENT_LENGTH} > $cf{maxdata});
		read(STDIN, $buf, $ENV{CONTENT_LENGTH});
	} else {
		$buf = $ENV{QUERY_STRING};
	}
	foreach ( split(/&/, $buf) ) {
		my ($key,$val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# ������
		$val =~ s/["'<>&\r\n]//g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	return %in;
}

#-----------------------------------------------------------
#  �p�X���[�h�F��
#-----------------------------------------------------------
sub check_passwd {
	# �p�X���[�h�������͂̏ꍇ�͓��̓t�H�[�����
	if ($in{pass} eq "") {
		&enter_form;

	# �p�X���[�h�F��
	} elsif ($in{pass} ne $cf{password}) {
		&error("�F�؂ł��܂���");
	}
}

#-----------------------------------------------------------
#  �������
#-----------------------------------------------------------
sub enter_form {
	&header("�������");
	print <<EOM;
<div style="margin-top:4em;text-align:center;">
<form action="$cf{admin_cgi}" method="post">
<table width="380">
<tr>
	<td height="40" align="center">
		<fieldset><legend>�Ǘ��p�X���[�h����</legend>
		<br>
		<input type="password" name="pass" value="" size="20">
		<input type="submit" value=" �F�� ">
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
#  �G���[����
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
#  HTML�w�b�_�[
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
<title>���J�E���^</title>
</head>
<body>
EOM
}

#-----------------------------------------------------------
#  �߂�{�^��
#-----------------------------------------------------------
sub back_btn {
	print <<EOM;
<div align="right">
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="&lt; ���j���[">
</form>
</div>
EOM
}

#-----------------------------------------------------------
#  ���b�Z�[�W�\��
#-----------------------------------------------------------
sub message {
	my ($msg, $param) = @_;

	&header("��������");
	print <<EOM;
<span style="color:#008000">$msg</span>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="$param" value="1">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="�����̃t�H�[���ɖ߂�" style="width:160px">
</form>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<input type="submit" value="�Ǘ����j���[�ɖ߂�" style="width:160px">
</form>
</body>
</html>
EOM
	exit;
}

