import waybackmach as wb
from urllib.parse import urlparse
import re
import sys
def urlhostname(urlishere):
    return urlparse(urlishere).hostname

def urlpathname(urlishere):
    return urlparse(urlishere).path

#domain = "*.jora.com"
domain = sys.argv[1]

urlsfullist = []
Subdomainls = []
Specials = []

#WayBackMachine Section
wbm = wb.waybackMachineClass(domain)
WayBackUrlsList = wbm.getUrls().strip().split('\n')
urlsfullist.extend(WayBackUrlsList)

urlsfullist = list(dict.fromkeys(urlsfullist)) # to remove duplicates
for y in urlsfullist:
    if urlparse(y).hostname[:4] == "www." :
        #myindex = WayBackUrlsList.index(y)
        #print("Found ", y)
        urlsfullist[urlsfullist.index(y)] = y.replace("www.","",1)
        #print(WayBackUrlsList[myindex])


SortedList = sorted(urlsfullist, key=lambda x: (urlhostname(x), urlpathname(x)))


for url in urlsfullist:
    prsdurl = urlparse(url)
    if prsdurl.port not in [None, 443, 80] or prsdurl.scheme.strip() not in ["http", "https", prsdurl.hostname.strip(), ""]:
        Specials.append(prsdurl.geturl())
    subdomain = str(str(prsdurl.scheme) + '://' + str(prsdurl.hostname)).strip("./\\?%$&*@#!-=+^`~")
    if subdomain not in Subdomainls:
        #print(url)
        #print(subdomain)
        Subdomainls.append(subdomain)


# Special Urls Alert
if len(Specials) != 0:
    print ("ALEERTT SPECIALS HAS GOT INTO SOMETHING !!! ")
    for thing in Specials:
        print(thing)

filename = str(domain + "all.txt")
extensionsfile = str(domain + "ext.txt")
subdomainsfile = str(domain + "subs.txt")
with open(filename, 'w') as writer:
    #print("Creating/Overwriting new File with name : ", filename)
    writer.write("") # This will overwrite anyexisting text.
   # print(": : : Printing : : : \n")
for l in SortedList:
    print(l)
    with open(filename, 'a') as writer:
        writer.write(f'{l} \n')

with open(subdomainsfile, "w") as writee:
    for kk in Subdomainls:
        writee.write(f'{kk} \n')




# gettiing extensions out of the urls

filesurl = []
pattern = r'\b/.+?\..+?\b$'
for urlext in urlsfullist:
    if re.search(pattern,urlext) != None :
        filesurl.append(urlext)
        print(urlext)

with open(extensionsfile, 'w') as writerext:
    for kkk in filesurl:
        writerext.write(f'{kkk} \n')