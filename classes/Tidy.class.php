<?php

class Tidy {
    public $tc;

    public function __construct($tc){
        $this->tc=$tc;

        if(count($_GET)==0){
            //$this->defaultForms();
        }//if

        $this->tc->pushHTML('
            <div id="results"></div>');

    }//construct

    private function defaultForms(){
        $this->tc->pushHTML('
            <form id="do-tidy">
                <label>URL</label>
                <input type="text" length="200" name="url">
                <label>Only do a specific style sheet (optional)</label>
                <input type="text" length="200" name="stylesheet">
                <div id="submit-tidy"><div>Tidy</div></div>
            </form>
            ');

    }//defaultForms

}//class Tidy

?>
