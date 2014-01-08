<?php

$tidyPath = dirname(__FILE__).'/codebase/';

if(isset($_POST['url'])){

    if(!isset($_GET['run'])){
        printOutput();
    }//if
    else {
        run();
    }//el

}//if
else if(isset($_GET['checkIfRan'])){
    $baseName = parse_url($_GET['url'])['host'];
    if(is_dir($tidyPath.'newcss/'.$baseName)){
        echo '1';
    }//if
    else {
        echo '0';
    }//el
}//elif

function run(){
    global $tidyPath;
    $args =  $_POST['url'];
    if(isset($_POST['stylesheet'])){
        $args.=' '.$_POST['stylesheet'];
    }//if

    $exec = "python {$tidyPath}parse.py $args";
    $done = shell_exec($exec);

    printOutput();

}//run

function printOutput(){
    global $tidyPath;
    $baseName = parse_url($_POST['url'])['host']; 
    $filePath = "{$tidyPath}newcss/{$baseName}/output.html";


    if(is_file($filePath)){
        echo file_get_contents($filePath);
    }//if 
    else {
        echo '<h3>Problem reading output file<h3><p>Please re-run tidy to fix</p>';
    }//el
}//printOutput


?>
