var endPoint='http://tidymycss.localhost/';
var tidyUrl = '';

$(document).ready(function(){
    $(window).bind('resize',flex);
    flex();
});

function flex(){
    $('#right-page').css('margin-top',$('#left-page').height());
}//flex

var form = {

    listen: function(){
        $('body').on('click','#submit-tidy',function(){

            tidyUrl = $("input[name='url']").val();
            $('#submit-tidy').hide();
            form.checkRunStatus();
        });
    }(),//listen
    checkRunStatus: function(){
        $.ajax({
            url:endPoint+'ajaxPortal.php?checkIfRan&url='+tidyUrl,
            type:'GET',
            success: function(data){
                var fhtml = 
                '<div id="pop-message">'
                    +'<div>'
                        +'<p>It appears you have already done a tidy of your css</p>'
                        +'<p>Would you like to view the past results or do a re-run?</p>'
                        +'<div onclick="form.request(\'run\')">Re-run</div>'
                        +'<div onclick="form.request()">View old</div>'
                    +'</div>'
                +'</div>';
                    
                if(data=='0'){
                    form.request('run');
                }//if
                else {
                    $('#do-tidy').after(fhtml);
                }//el
            }
        });

    },//checkRunStatus
    request: function(type){
        type = type || "";

        $('#pop-message').remove();
        $('#results').html('<div id="loading-wrapper"><img src="/images/loading.gif"/></div>');

        $.ajax({
            url:endPoint+'ajaxPortal.php?'+type,
            type:'POST',
            data:$('#do-tidy').serialize(),
            success: function(data){
                $('#results').html(data);
                $('.css-index').eq(0).addClass('active');
                $('#files > div').eq(0).addClass('active');

                $('#files > div').each(function(){
                    var n  = $(this).children('p').eq(0).text();
                    n = n.split('/').join('-');
                    n = n.substr(1,n.length);
                    var link = '<a target="_blank" href="'+endPoint+'getFile.php?url='+tidyUrl+'&file='+n+'"></a>';
                    var nfLink = '<a target="_blank" href="'+endPoint+'getFile.php?url='+tidyUrl+'&file=notfound.'+n+'"></a>';
                    $(this).children('.imageWrap').eq(0).children('img').wrap(link);
                    $(this).children('.imageWrap').eq(1).children('img').wrap(nfLink);
                    $('#submit-tidy').show();
                });
            }
        });
    }//request

}

$('body').on('click','.view-pages',function(){
    $(this).parent().children('.pages').toggle();
});

var file = {

    init:function(){
        $('body').on('click','.aFile',function(){
            var index = $('.aFile').index(this);
            var show = $('.css-index').eq(index);
            $('.css-index').removeClass('active');
            $(show).addClass('active');
            $('#files > div').removeClass('active');
            $('#files > div').eq(index).addClass('active');
        });

    }(),
    show:function(){

    }
}
