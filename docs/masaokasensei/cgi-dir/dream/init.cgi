# ���W���[���錾/�ϐ�������
use strict;
my %cf;
#��������������������������������������������������������������������
#�� DreamCounter : init.cgi - 2011/09/27
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$cf{version} = 'DreamCounter v4.1';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#��������������������������������������������������������������������
#
# [ �^�O�̏������̗� ]
#
#  �E�J�E���^ <img src="http://�`/dream.cgi?id=[���OID��]">
#  �E�����\�� <img src="http://�`/dream.cgi?mode=time">
#  �E�J�����_ <img src="http://�`/dream.cgi?mode=date">
#  �E�t�@�C���̍X�V����
#             <img src="http://�`/dream.cgi?file=/home/�`/index.html">
#             [����] "/home/�`/index.html" �̕����̓t���p�X�w��
#
#  * ���p�� (���OID���� index �Ɖ���)
#    1.�摜��ύX����Ƃ��F(�ȉ���gif2�f�B���N�g���̉摜�w���)
#      <img src="http://�`�`/count/dream.cgi?id=index&gif=2">
#    2.�����������_���ɕ\������Ƃ��F
#      <img src="http://�`�`/count/dream.cgi?mode=rand">
#    3.�J�E���^������7���ɂ���Ƃ��F
#      <img src="http://�`�`/count/dream.cgi?id=index&fig=7">

#===========================================================
# �� ��{�ݒ�
#===========================================================

# �Ǘ��p�X���[�h�i�p�����Ŏw��j
$cf{password} = 'pass123';

# �摜�A�����W���[��
# 0 : gifcat.pl
# 1 : Image-Magick�i�T�[�o�ɃC���X�g�[������Ă���K�v����j
$cf{image_pm} = 0;

# IP�A�h���X�̃`�F�b�N (0=no 1=yes) 
#  �� yes�̏ꍇ�A������IP�A�h���X�̓J�E���g�A�b�v���Ȃ�
$cf{ip_chk} = 1;

# ���O��u���T�[�o�f�B���N�g��
# �� ���s�f�B���N�g���ł���΂��̂܂܂ł悢
$cf{datadir} = './data';

# ���T�C�g����A�N�Z�X��r��
#  �� �r������   : dream.cgi��ݒu����URL�� http://����L�q
#  �� �r�����Ȃ� : �����L�q���Ȃ��i���̂܂܁j
#   ���F�������u�r������v�Ƃ����ꍇ�A�ݒu����T�[�o�◘�p�҂̃u���E�U
#       �ɂ���Ă͎��T�C�g����ł��A�N�Z�X��r������ꍇ������܂��B
$cf{base_url} = "";

# �摜�̂���f�t�H���g�i�����l�j�̃f�B���N�g���w��y�T�[�o�p�X�z
$cf{gifdir} = './gif1';

# �����w��̍ő�l�i�Z�L�����e�B�΍�j
#   �� ����𒴂��錅���͎w�肵�Ă���������܂��B
$cf{maxfig} = 12;

# �{��CGI�yURL�p�X�z
$cf{dream_cgi} = './dream.cgi';

# �Ǘ�CGI�yURL�p�X�z
$cf{admin_cgi} = './admin.cgi';

# gifcat.pl�̃p�X�y�T�[�o�p�X�z
$cf{gifcat_pl} = './lib/gifcat.pl';

# magick.pl�̃p�X�y�T�[�o�p�X�z
$cf{magick_pl} = './lib/magick.pl';

# �Ǘ���ʂ̍ő�󗝃T�C�Y�i�o�C�g�j
$cf{maxdata} = 10240;

#===========================================================
# �� �ݒ芮��
#===========================================================

# �ݒ�l��Ԃ�
sub init { return %cf; }


1;

