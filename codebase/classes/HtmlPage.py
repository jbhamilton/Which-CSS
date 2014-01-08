from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select
import urllib 
from urlparse import urlparse
import re


def setHostName(n,f):
    global urlHostName
    urlHostName = n 
    global filePath
    filePath = f 
    

class HtmlPage:

    def __init__(self,ID,vurl):
        self.pageID = ID
        self.url = vurl
        self.parsed = False

        self.html = Soup(urllib.urlopen('http://'+urlHostName+self.url))
        self.styles = select(self.html,'link[rel="stylesheet"]')
        self.links = select(self.html,'a')
        self.jScripts = select(self.html,'script[type="text/javascript"]')

        self.links = self.listToLocalOnly(self.links)
        self.styles = self.listToLocalOnly(self.styles)
        self.jScripts = self.listToLocalOnly(self.jScripts)

        print 'Parsing page ',vurl,' with ID of: ',ID
        print 'Page has ',len(self.links),' links'
        print '-'*30


    def listToLocalOnly(self,list):
        newList = []
        for l in list:
            try:
                urlParts = urlparse(l['href'])
            except KeyError:
                urlParts = urlparse(l['src'])


            q = ''
            if urlParts.query!='':
                q = '?'+urlParts.query

            if urlParts.hostname == urlHostName or urlParts.hostname==None or urlParts.hostname=='':

                baseParts = urlparse(self.url)

                firstChar = urlParts.path[0:1]
                firstTwoChar = urlParts.path[0:2]
                
                lasPos = baseParts.path.rfind('/')
                if lasPos == -1:
                    lasPos = len(baseParts.path) 
                else:
                    lasPos+=1
                
                base = baseParts.path[0:lasPos]
                
                
                if firstChar=='/':
                    newList.append(urlParts.path+q)
                elif re.search('[a-zA-Z0-9\-]',firstChar):
                    newList.append(base+urlParts.path)
                elif firstTwoChar=='./':
                    newList.append(base+urlParts.path[2:])
                elif firstTwoChar=='..':
                    c = urlParts.path.count('../')
                    base = base[0:len(base)-1]
                
                    for i in range(c):
                        base = base[0:base.rfind('/')]
                
                    base+='/'
                
                    newList.append(base+urlParts.path[c*3:])
    
        return newList


class jScriptFile:

    def __init__(self,path):
        self.url = path
        self.sourceCode = urllib.urlopen('http://'+urlHostName+path).read()

        self.strings = self.getStrings()

    def getStrings(self):
        
        pattern1 = re.compile('\"+([a-zA-Z0-9\-\_\s\'\<\=\>\/\.]+)\"+')
        pattern2 = re.compile('\'+([a-zA-Z0-9\-\_\s\"\<\=\>\/\.]+)\'+')
        

        matches1 = list(pattern1.finditer(self.sourceCode))
        matches2 = list(pattern2.finditer(self.sourceCode))
        
        
        matches1.extend(matches2);
        
        
        matches1.sort(key=lambda x: x.start())
        
        presoup = [m.group(0) for m in matches1]
        presoup = ' '.join(presoup)
        
        return Soup(presoup)


    def findString(self,string):
        if string =='' or string==None:
            return False

        badPsuedos = [':active',':link',':visited',':hover',':focus',':first-letter',':first-line',':first-child',
                ':before',':after',':first-of-type',':last-of-type',':only-of-type',':only-child',':last-child',':empty',]
                
        for b in badPsuedos:
            if b in string:
                string.replace(b,'')

        try:
            r = select(self.strings,string)
            return r
        except IndexError as e:
            print e
            print string
            return False



class CssFile:
    def __init__(self,path):
        self.path = path
        self.pages = []
        self.pageObjects = []
        self.tagObjects = []
        self.css = self.getCssFile()
        self.fileExists = True

        if re.search('<\/.{1,25}>',self.css):
            self.fileExists = False


    def getCssFile(self):
        url = 'http://'+urlHostName+self.path
        print 'about to get css file with path: ',url
        return urllib.urlopen(url).read()

    def addPageID(self,ID):
        self.pages.append(ID)

    def addPage(self,page):
        self.pageObjects.append(page)

    def buildCssObject(self,css):
        self.cssObject = css
        for rule in css.rules:
            self.tagObjects.append(Tag(rule))

    # accepts a html as string object
    def verifyHtml(self,html):
        #reg = '((class|id)=\")[a-zA-Z0-9\-\_\s]*({})[a-zA-Z0-9\-\_\s]*(\")'

        for tag in self.tagObjects:
            if tag.found:
                continue
            for i,t in enumerate(tag.tags):
                if t.find('*')!=-1:
                    tag.found = True
                    continue
                if t.find(':')!=-1:
                    tag.found = True
                    continue

                #print 'finding matches for :',t
                matches = []
                try:
                    matches = select(html,t)
                except IndexError as e:
                    #print 'Error finding matches',e
                    tag.found = True
                    tag.tagsFound[i] = True 

                if len(matches)>0:
                    tag.found = True
                    tag.tagsFound[i] = True 
                    #print 'Found Match(s)'
                else:
                    pass
                    #print 'No Match!'

    def createNewCssFile(self):
        if not self.fileExists:
            return

        foundFile = ''
        notFoundFile = ''
        for tag in self.tagObjects:
            if len(tag.tags)==0:
                continue

            tags = ','.join(tag.tags)+' {\n'

            props = ''
            for p in tag.properties.declarations:
                props+=str(p.name)+':'+str(p.value.as_css())+';\n'
            props+='} \n'

            if tag.found:
                foundFile+=tags+props 
            else:
                notFoundFile+=tags+props

        #write out the found css properties
        fo = open(filePath+urlHostName+'/'+((self.path).replace('/','-')[1:]),'wb')
        fo.write(foundFile)
        fo.close()

        #write out the not found css properties
        fo = open(filePath+urlHostName+'/notfound.'+((self.path).replace('/','-')[1:]),'wb')
        fo.write(notFoundFile)
        fo.close()



class Tag:
    def __init__(self,rule):
        self.found = False
        self.tags = []
        self.tagsFound = []
        self.foundInScript = []
        self.scriptNames = []
        self.properties = rule
        if rule.at_keyword  == '@media':
            self.found = True
            return
        elif rule.at_keyword == '@page':
            self.found = True
            return

        try:
            sr = rule.selector.as_css()
            if sr.find(',')==-1:
                self.tags.append(sr)
                self.tagsFound = [False]
            else:
                self.tags.extend(sr.split(','))
                self.tagsFound = [False]*len(sr.split(','))
        except AttributeError as e:
            print 'AttributeError ',e

    def printUsed(self):
        info = '<ul class="tags">'
        infohtml = '<li class="{}">{}</li>' 
        if len(self.tags)>1:
            for i,t in enumerate(self.tags):
                fType = ''
                if i in self.foundInScript:
                    fType = '<span class="foundInScript" title="'+self.scriptNames[self.foundInScript.index(i)]+'">*</span>'
                info+= infohtml.format(str(self.tagsFound[i]),fType+str(t))
        else:
            info+= infohtml.format(str(self.found),str(self.tags[0]))

        return info+'</ul>'

    def printProperties(self):
        props = '<p class="properties">'
        for p in self.properties.declarations:
            props+=str(p.name)+':'+str(p.value.as_css())+';</br>'
        props+='</p>'
        return props
