<?php

class Tidy {
    public $tc;

    public function __construct($tc){
        $this->tc=$tc;

        if(count($_GET)==0){
            $this->defaultForms();
        }//if

        $this->tc->pushHTML('
            <div id="results"></div>');

    }//construct

    private function defaultForms(){
        $this->tc->pushHTML('
            <form id="do-tidy">
                <label>URL</label>
                </br>
                <input type="text" length="100" name="url">
                </br>
                <label>Only do a specific style sheet (optional)</label>
                </br>
                <input type="text" length="100" name="stylesheet">
                <div id="submit-tidy">Tidy</div>
            </form>
            ');

    }//defaultForms

}//class Tidy

?>
