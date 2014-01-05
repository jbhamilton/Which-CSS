<?php

$tidyPath = 'codebase/newcss/';

$fileName = parse_url($_GET['url'])['host'];
$file = (substr($_GET['file'],0,1)=='-') ? substr($_GET['file'],1,strlen($_GET['file'])) : $_GET['host']; 
$file = str_replace('/','-',$file);
$fileName =$tidyPath.$fileName.'/'.$file;


if (!file_exists($fileName)) trigger_error("File '$fileName' doesn't exist.", E_USER_ERROR);

header("X-Sendfile: $fileName");
header("Content-type: application/octet-stream");
header('Content-Disposition: attachment; filename="' . basename($fileName) . '"');

?>
