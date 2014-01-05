<?php

$tidyPath = '/home/bballer/Scripts/Python/cssPerfect/';
$exec = "python {$tidyPath}parse.py http://www.revampify.com";
echo shell_exec($exec);


?>
