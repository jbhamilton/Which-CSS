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

        self.links = self.listToLocalOnly(self.links)
        self.styles = self.listToLocalOnly(self.styles)

        print 'Parsing page ',vurl,' with ID of: ',ID
        print 'Page has ',len(self.links),' links'
        #print self.links
        print '-'*30


    def listToLocalOnly(self,list):
        newList = []
        for l in list:
            urlParts = urlparse(l['href'])
            #print l['href']
            #print urlParts
            q = ''
            if urlParts.query!='':
                q = '?'+urlParts.query

            if urlParts.hostname == urlHostName or urlParts.hostname==None:
                if urlParts.path.find('/')==-1:
                    pos = self.url.rfind('/')
                    if pos==-1:
                        nurl = self.url+'/'
                    else:
                        nurl = self.url[0:pos+1]
                    newList.append(nurl+urlParts.path+q)
                if urlParts.hostname==None:
                    i = (urlParts.path).find('/')
                    newList.append(urlParts.path[i:]+q)
                else :
                    newList.append(urlParts.path+q)
    
        return newList






class CssFile:
    def __init__(self,path):
        self.path = path
        self.pages = []
        self.pageObjects = []
        self.tagObjects = []
        self.css = self.getCssFile()

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

                print 'finding matches for :',t
                matches = []
                try:
                    matches = select(html,t)
                except IndexError as e:
                    print 'Error finding matches',e
                    tag.found = True
                    tag.tagsFound[i] = True 

                if len(matches)>0:
                    tag.found = True
                    tag.tagsFound[i] = True 
                    print 'Found Match(s)'
                else:
                    print 'No Match!'

    def createNewCssFile(self):
        fo = open(filePath+urlHostName+'/'+((self.path).replace('/','-')[1:]),'wb')
        for tag in self.tagObjects:
            if len(tag.tags)==0 or not tag.found:
                continue

            fo.write(','.join(tag.tags)+' {\n')

            props = ''
            for p in tag.properties.declarations:
                props+=str(p.name)+':'+str(p.value.as_css())+';\n'
            props+='} \n'

            fo.write(props)

        fo.close()



class Tag:
    def __init__(self,rule):
        self.found = False
        self.tags = []
        self.tagsFound = []
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
                info+= infohtml.format(str(self.tagsFound[i]),str(t))
        else:
            info+= infohtml.format(str(self.found),str(self.tags[0]))

        return info+'</ul>'

    def printProperties(self):
        props = '<p class="properties">'
        for p in self.properties.declarations:
            props+=str(p.name)+':'+str(p.value.as_css())+';</br>'
        props+='</p>'
        return props
