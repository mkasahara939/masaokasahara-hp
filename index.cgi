#!/usr/bin/perl

#ǯ�����μ����Υ���ץ�
my($sec, $min, $hour, $day, $mon, $year, $wday) = localtime(time);
$mon  += 1;
$year += 1900;

#�Ķ��ѿ�������ɽ�������ѤΥ���ץ�
$name = $ENV{"REQUEST_URI"};
$name =~ s/\/([\w\-]+)\/.*/$1/g;

#ifʸ�Υ���ץ�
if(length($name) > 2){
  $name .= "����";
}else{
  $name = "";
}

#�إå��ν��ϤΥ���ץ�
print "Content-type: text/html\n\n";

#HTML�ν��ϤΥ���ץ�

print <<EOL; 
<html><head><!--��-->
<META HTTP-EQUIV="content-type" CONTENT="text/html; charset=euc-jp">
<title>Yahoo!�������ƥ����� - CGI����ץ�ڡ���</title></head>
<body>
<center>
<br>
<p>
<h1>CGI����ץ�ڡ���</h1>
<b>����ˤ���$name</b>
<hr size=1 width=500>
<table width=500 border=0 cellspacing=0 cellpadding=4>
<tr>
<td width="1%">
<img src="http://pic.geocities.jp/images/members/default/nmi.gif" border="0" hspace="2" width="41" height="20">
</td>
<td>
�����ץ饹�ʤ顢�����CGI�򤴻��Ѥ��������ޤ������ꥸ�ʥ�ηǼ��Ĥ䥢�󥱡��ȡ���ɼ�ʤɤγڤ�����ǽ��ۡ���ڡ������ɲä��Ƥߤ褦��
</td>
</tr>
</table>
</center>
</body>
</html>
EOL

