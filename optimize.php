<?php

require_once('tidycss/class.csstidy.php');

$cssCode = file_get_contents('codebase/newcss/www.bradleyhamilton.com/css-1140.css');

$css = new csstidy();

$css->parse($cssCode);
$css->optimise->value();
$css->optimise->shorthand();
$css->optimise->shorthands();
$css->optimise->subvalue();

file_put_contents('codebase/newcss/www.bradleyhamilton.com/optimized.css-1140.css',$css->print->plain());


?>
