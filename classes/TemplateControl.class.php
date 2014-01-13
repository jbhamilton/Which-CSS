<?php
ini_set('display_errors',1);
error_reporting(E_ALL);


class templateControl {
    public $ctrl;
    public $html = Array();
    public $scripts = Array();
    public $styles = Array();
    public $title;
    public $description;
    public $currentPage;
    public $path = 'http://tidymycss.localhost/';

    public function __construct($ctrl=null){
        $this->ctrl = $ctrl;
        $this->title = "Clean up your CSS - Find used selectors, generate new CSS files | TidyMyCSS";
        $this->description = "'CSS cleaning'";


    }//construct

    public function setTitle($t){
        $this->title=$t;
    }//setTitle

    public function setDesc($d){
        $this->description=$d;
    }//setDesc

    public function  pushHTML($p){
        $this->html[]=$p;
    }//pushHTML

    public function pushScript($s){
        $this->scripts[]=$s;
    }//pushScript

    public function pushStyle($s){
        $this->styles[]=$s;
    }//style

    private function printScripts(){
        $scripts='<script type="text/javascript">';
        foreach($this->scripts as $s){
            $scripts.=$s;
        }//foreach
        return $scripts.'</script>';
    }//printScripts

    private function printStyles(){
        if(count($this->styles)==0){
            return '';
        }//if

        $styles='<style>';
        foreach($this->styles as $s){
            $styles.=$s;
        }//foreach
        return $styles.'</style>';
    }//printStyles

    //this function handles printing the entire page
    public function printPage(){

        echo $this->buildMetaHeader();

        echo '<div id="right-page">'
            .'<div id="body">';

        $this->HTMLDump();

        echo '</div>';//close #body
        echo '</div>';//close #right-page

        //print the navigation
        echo $this->nav();

    }//printPage

    public function HTMLDump(){
        foreach($this->html as $p){
            echo $p;
        }//foreach
    }//HTMLDump

    public function nav(){
        
        $nav = "
            <div id='left-page'>
                <div class='logoHolder'>
                    <img src='{$this->path}images/logo.png' alt='Which Css'/>
                </div>

                <form id='do-tidy'>
                    <label>URL</label>
                    <input type='text' length='200' name='url'>
                    <label>Only do a specific style sheet (optional)</label>
                    <input type='text' length='200' name='stylesheet'>
                    <div id='submit-tidy'><div>Tidy</div></div>
                </form>

                <div class='clear'></div>

            </div>

            <script type='text/javascript' src='%1\$sscripts/js.js'></script>
            </body>
         </html>";
 
        return sprintf($nav,$this->path);

    }//nav


    public function buildMetaHeader(){

        $metaHeader = <<<HEAD
<!doctype html>
    <html lang="en">
        
    <head>
        <meta charset="utf-8" />
        
        
        <meta content="index,follow" name="robots">
        
        <title> %1\$s </title>
        <meta name="description" content=%2\$s>
        
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

        <link type="image/x-icon" href="{$this->path}waveleak_favicon.png" rel="shortcut icon">
        <link href='http://fonts.googleapis.com/css?family=Alegreya+Sans' rel='stylesheet' type='text/css'>
        
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js" type="text/javascript"></script>
        
        
        <!--[if IE]>
        <script type="text/javascript">var isIE=true;</script>
        <![endif]-->
        <!--[if lte IE 8]>
            <script type="text/javascript">window.location='http://www.waveleak.com/why-no-ie-less-than-9';</script>
        <![endif]-->

                    
        %3\$s
        %4\$s
        %5\$s
        	

        </head>
    <body>

HEAD;

            return sprintf($metaHeader,$this->title,$this->description,$this->printScripts(),$this->style(),$this->printStyles());

    }//buildMetaHeader

    private function style(){
        //return "<link rel='stylesheet' href='{$this->path}tmp/styles.css' type='text/css' media='screen and (min-device-width: 800px)'/>";
        return "<link rel='stylesheet' href='{$this->path}css/css.css' type='text/css'/>";
    }//styleTesting


}//templateControl


?>
