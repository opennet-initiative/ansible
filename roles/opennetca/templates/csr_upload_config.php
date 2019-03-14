<?php
// config variables
$debug = false;
$allowedExts = array("csr");
$allowedType = array(
  "application/octet-stream",
  "application/pkcs10",
  "text/opennet_csr");
$uploadFolder = "{{ opennetca_path_csr }}";
$cnFilter = array(
{% for item in opennetca_list %}
{% set cn_list = item.cn.split(' ') %}
{% for cn in cn_list %}
  "{{ cn }}" => "{{ item.ca }}",
{% endfor %}
{% endfor %}
  "" => ""
);
$mailto = "Opennet CSR Team <{{ opennetca_mail_csrto }}>";
$mailfrom = "Opennet CA <opennetca@opennet-initiative.de>";
$mailsubject = "Opennet CA (upload): Signing Request / Zertifikatsanfrage";
$mailfooter = "-- \r\nOpennet Initiative e.V.\r\nhttps://www.opennet-initiative.de\r\nCA Status: {{ opennetca_mail_url }}";
$approveurl = "{{ opennetca_mail_url }}/internal/csr_approve.php?";
?>
