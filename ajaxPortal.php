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
    if(is_dir($tidyPath.'newcss/'.$_GET['url'])){
        echo '1';
    }//if
    else {
        echo '0';
    }//el
}//elif

function run(){
    $args =  $_POST['url'];
    if(isset($_POST['stylesheet'])){
        $args.=' '.$_POST['stylesheet'];
    }//if

    $exec = "python {$tidyPath}parse.py $args";
    $done = shell_exec($exec);

    printOutput();

}//run

function printOutput(){
    $baseName = parse_url($_POST['url'])['host']; 
    echo file_get_contents("{$tidyPath}newcss/{$baseName}/output.html");
}//printOutput


?>
