<?php

$tidyPath = 'codebase/newcss/';

if(!isset($_GET['url']) || !isset($_GET['file'])){
    echo 'not found';
    exit(0);
}//if

$fileName = parse_url($_GET['url'])['host'];
$file = (substr($_GET['file'],0,1)=='-') ? substr($_GET['file'],1,strlen($_GET['file'])) : $_GET['host']; 
$file = str_replace('/','-',$file);
$fileName =$tidyPath.$fileName.'/'.$file;


if (!file_exists($fileName)){
    echo 'not found';
   
    trigger_error("File '$fileName' doesn't exist.", E_USER_ERROR);
    exit(0);
}//if


header("X-Sendfile: $fileName");
header("Content-type: application/octet-stream");
header('Content-Disposition: attachment; filename="' . basename($fileName) . '"');

?>
