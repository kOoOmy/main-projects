import requests
import sys


domainy = sys.argv[1]
#domainy = "*.magisto.com"
#domainy = "*.nepalstock.com/*"
class waybackMachineClass():

        def __init__(self,domain):
                self.waybackURL = "https://web.archive.org/cdx/search?url="+domain+"&output=text&fl=original&collapse=urlkey"
                self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        def getUrls(self):
                r = requests.get(self.waybackURL,headers=self.headers)
                html = r.text
                return html


wbm = waybackMachineClass(domainy)
urls = wbm.getUrls()
urlist = urls.split('\n')
print(urlist)
