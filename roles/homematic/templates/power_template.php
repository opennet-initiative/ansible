<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Opennet Initiative e.V.</title> 
</head>
<body>
<h1>Frieda23 - Schalte Steckdose {{ item.de }} / Switch Power Socket {{ item.en }}</h1>

<table cellpadding="15" cellspacing="0">
<tr>
<td align="center">
  <img src="/power_{{ item.task }}.png">
</td>
</tr>
<tr bgcolor="#eeeeee">
<td>
  <pre>
<?php echo shell_exec('{{ homematic_path_user }}/homematic.sh --power-{{ item.task }}'); ?>
  </pre>
</td>
</tr>
</table>

<p>
<a href="/">Zurück zur Startseite</a>
<p>
<img src="/Opennet_logo_quer.gif" alt="Opennet Logo">
<img src="/sl-logo_0.jpg" alt="Senselab Logo">
</p>

</body>
</html>
