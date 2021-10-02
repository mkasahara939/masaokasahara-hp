#!/usr/bin/perl

#年月日の取得のサンプル
my($sec, $min, $hour, $day, $mon, $year, $wday) = localtime(time);
$mon  += 1;
$year += 1900;

#環境変数と正規表現の利用のサンプル
$name = $ENV{"REQUEST_URI"};
$name =~ s/\/([\w\-]+)\/.*/$1/g;

#if文のサンプル
if(length($name) > 2){
  $name .= "さん。";
}else{
  $name = "";
}

#ヘッダの出力のサンプル
print "Content-type: text/html\n\n";

#HTMLの出力のサンプル

print <<EOL; 
<html><head><!--京-->
<META HTTP-EQUIV="content-type" CONTENT="text/html; charset=euc-jp">
<title>Yahoo!ジオシティーズ - CGIサンプルページ</title></head>
<body>
<center>
<br>
<p>
<h1>CGIサンプルページ</h1>
<b>こんにちは$name</b>
<hr size=1 width=500>
<table width=500 border=0 cellspacing=0 cellpadding=4>
<tr>
<td width="1%">
<img src="http://pic.geocities.jp/images/members/default/nmi.gif" border="0" hspace="2" width="41" height="20">
</td>
<td>
ジオプラスなら、自作のCGIをご使用いただけます。オリジナルの掲示板やアンケート、投票などの楽しい機能をホームページに追加してみよう！
</td>
</tr>
</table>
</center>
</body>
</html>
EOL

