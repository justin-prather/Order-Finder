import mechanize
import urllib
from time import sleep
#Make a Browser (think of this as chrome or firefox etc)
br = mechanize.Browser()
links = { 'Order of Go':[], 'Results': []}

#visit http://stockrt.github.com/p/emulating-a-browser-in-python-with-mechanize/
#for more ways to set up your br browser object e.g. so it look like mozilla
#and if you need to fill out forms with passwords.

# Open your site
br.open('http://www.sprucemeadows.com/tournaments/orderAndGo.jsp?id=19&d=2013-05-05&ty=2013')

for link in br.links():
    if '.pdf' in link.url:
        if link.text == 'Order of Go':
            links['Order of Go'].append( 'http://www.sprucemeadows.com/tournaments/' + link.url )
        elif link.text == 'Results':
            links['Results'].append( 'http://www.sprucemeadows.com/tournaments/' + link.url )


for i in links['Order of Go']:
    print 'downloading: ' + i
    urllib.urlretrieve( i, 'Orders/' + i[61:-4] + '.pdf')