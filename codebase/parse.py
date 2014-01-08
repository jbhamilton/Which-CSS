from urlparse import urlparse
from tinycss.css21 import CSS21Parser
import sys
import classes.HtmlPage as HtmlPage
import classes.PagePrinter as PagePrinter
import os

filePath = os.path.dirname(os.path.realpath(__file__))+'/newcss/' 
pageCounter = 1

pageObjects = []
pagesVisited = []
cssVisited = []
cssObjects = []
jScriptObjects = []
jScriptVisited = []

# obtain the url from args that we need to parse
try:
    url = sys.argv[1] 
except IndexError:
    #url = 'http://www.bradleyhamilton.com'
    sys.exit('You must enter a URL to parse')  

try:
    certainStyleSheet = sys.argv[2]
except IndexError:
    certainStyleSheet = None 

# get the url parts
urlParts = urlparse(url)
# set the base hostname in the HtmlPage module
HtmlPage.setHostName(urlParts.hostname,filePath)

#make the directory for the site
#if it doesn't exist
mdir = filePath+urlParts.hostname
if not os.path.exists(mdir):
    os.makedirs(mdir)
    os.chmod(mdir,0777)

# create the home page object 
# and append it to the pageObjects list
pageObjects.append(HtmlPage.HtmlPage(pageCounter,urlParts.path))


# This method allows us to add a page object 
# to a css object so we have a backwards reference
def addPageToCss(path,page):
    for css in cssObjects:
        if css.path == path:
            css.addPage(page)
            return


badExts = ['.jpg','.jpeg','.png','.pdf','@']

deadLinks = []

# go get all the pages on the website 
i = 0
while i < len(pageObjects):
    page = pageObjects[i]
    if not page.parsed:
        page.parsed = True

        for link in page.links:
            if [True for e in badExts if e in link] :
                print 'found bad extension'
                continue

            if link == '' or link == None:
                continue

            if not link in pagesVisited and not link in deadLinks:
                print 'visiting link ',link
                try:
                    pageObjects.append(HtmlPage.HtmlPage(pageCounter,link))
                    pagesVisited.append(link) 
                    pageCounter+=1
                except IOError:
                    print 'dead link'
                    deadLinks.append(link)



    i+= 1

#exception for handling only a user specified stylesheet
class BreakTheLoops(BaseException): pass

try:
    for i,page in enumerate(pageObjects):

        # go get all the css files on the website
        # and create a list of all the pages that use them
        for style in page.styles:
            if style.find('/')==-1 or style == '' or style == None:
                continue
    
            if certainStyleSheet != None and certainStyleSheet in page.styles:
                cssObjects.append(HtmlPage.CssFile(certainStyleSheet))
                addPageToCss(certainStyleSheet,page)
                cssVisited.append(certainStyleSheet)
                raise BreakTheLoops()
    
            if not style in cssVisited:
                try:
                    cssObjects.append(HtmlPage.CssFile(style))
                    addPageToCss(style,page)
                    cssVisited.append(style)
                except IOError:
                    print 'dead css link'
            else:
                addPageToCss(style,page)
except BreakTheLoops:
    pass

#go get all the javascript files on the site
for i,page in enumerate(pageObjects):
    for script in page.jScripts:
        if not script in jScriptVisited:
            try:
                print 'Getting JavaScript file '+script
                jScriptObjects.append(HtmlPage.jScriptFile(script))
                jScriptVisited.append(script)
            except IOError:
                print 'dead jScript link'


parser = CSS21Parser()
#for each style sheet create a manipulatable object of the 
#   style sheet using tinycss class
for css in cssObjects:
    try:
        css.buildCssObject(parser.parse_stylesheet(css.css))
        #for each page associated with the css
        for page in css.pageObjects:
            #see if the css properities exist on the page
            css.verifyHtml(page.html) 
    except UnicodeDecodeError as e:
        print 'unicode decode error found'
        print '@ file with path: ',css.path
        print e 
        
#go verify unfound css properties don't exist in the javascript files
for css in cssObjects:
    for t in css.tagObjects:
        for i,tf in enumerate(t.tagsFound):
            #if the tag isn't found
            if not tf:
                #get the property
                string = t.tags[i]

                #look through the javascript
                for s in jScriptObjects:
                    if s.findString(string):
                        t.foundInScript.append(i)
                        t.scriptNames.append(s.url)
                        t.tagsFound[i]=True
                        break;




PagePrinter.cssInfoDump(cssObjects,urlParts,filePath)

for css in cssObjects:
    css.createNewCssFile()
