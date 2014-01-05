import os

t = '#body'

t = t[1:]

print t

l = ['blah','di','haa']
boos = [True,False,True]

for i,t in enumerate(l):
    print '<li>',i,t,str(boos[i]),'</li>'


nl = [False] * 5

print nl

print os.getcwd()
