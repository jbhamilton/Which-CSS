<?php

require_once('classes/TemplateControl.class.php');
require_once('classes/Tidy.class.php');

$tc = new TemplateControl();
$tidy = new Tidy($tc);

$tc->printPage();

?>
