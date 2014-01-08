# Debug function
def cssInfoDump(cssObjects,urlParts,path):
    fo = open(path+urlParts.hostname+'/'+'output.html',"wb")
    wrap = '''
        <div id="legend">
            Not Used <div id="not-used"></div>
            Used <div id="used"></div>
            Found in JavaScript File <div id="asterick">*</div>
        </div>
        <div id="files">
            {}
        </div>
        <div id="content">
            {}
        </div>

    '''
    info = '''
        <div class="css-index">
            {}
        </div>
    '''
    fileWrap = '''
        <div>
            <p class="aFile">{}</p>
            <div class="imageWrap found">
                <img src="images/css-green.png" title="CSS File with only properties that were found"/>
            </div>
            <div class="imageWrap notFound" title="CSS File with only properties that were not found">
                <img src="images/css-red.png"/>
            </div>
            {}
        </div>
    '''
    deadFileWrap = '''
        <div class="deadFile">
            <p class="aFile dead">{}</p>
            {}
        </div>
    '''

    files = ''
    content = ''
    for css in cssObjects:


        pinfo = '<p class="sub-heading view-pages">Pages using this style sheet <span>&#10095;</span></p><ul class="pages">'
        for page in css.pageObjects:
            if page.url=='' or page.url==None:
                continue
            pinfo+= '<li><span>'+page.url+'</span></li>'
        pinfo +='</ul>'

        tagDiv = ''
        for tag in css.tagObjects:
            if len(tag.tags)==0 or tag.properties==None or len(tag.tagsFound)==0:
                continue
            tagDiv += tag.printUsed() 
            tagDiv += tag.printProperties()



        if not css.fileExists:
            tagDiv = ''
            files+= deadFileWrap.format(css.path,pinfo)
        else:
            files+= fileWrap.format(css.path,pinfo) 
            
        content+= info.format(tagDiv)

    fo.write(wrap.format(files,content))
    fo.close()

