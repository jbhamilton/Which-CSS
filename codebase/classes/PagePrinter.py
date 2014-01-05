# Debug function
def cssInfoDump(cssObjects,urlParts,path):
    fo = open(path+urlParts.hostname+'/'+'output.html',"wb")
    wrap = '''
        <div id="legend">
            Not Used <div id="not-used"></div>
            Used <div id="used"></div>
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
            <div class="imageWrap">
                <img src="images/css.png"/>
            </div>
            {}
        </div>
    '''

    files = ''
    content = ''
    for css in cssObjects:

        tagDiv = ''
        for tag in css.tagObjects:
            if len(tag.tags)==0:
                continue
            tagDiv += tag.printUsed() 
            tagDiv += tag.printProperties()

        pinfo = '<p class="sub-heading view-pages">Pages using this style sheet</p><ul class="pages">'
        for page in css.pageObjects:
            #if len(page.tags)!=0:
            pinfo+= '<li>'+page.url+'</li>'
        pinfo +='</ul>'

        files+= fileWrap.format(css.path,pinfo) 

        content+= info.format(tagDiv)

    fo.write(wrap.format(files,content))
    fo.close()

