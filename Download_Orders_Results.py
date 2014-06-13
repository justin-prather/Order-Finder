import mechanize
import urllib
import datetime 
import os.path

class PDF_Downloader():

	def __init__(self):
		self.links = { 'Order of Go':[], 'Results':[] }
		self.filePath = str()
		self.Tournament_link = str()

	def gen_tournament_link( self, ID, date ):
		base_link = 'http://www.sprucemeadows.com/tournaments/orderAndGo.jsp?id='
		self.Tournament_link = base_link + str(ID) + date.strftime( '&d=%Y-%m-%d&ty=%Y' )
		return self.Tournament_link

	def get_PDF_links(self):
		br = mechanize.Browser()
		try:
			br.open( self.Tournament_link )
		except mechanize.URLError:
			return False

		for link in br.links():
			if '.pdf' in link.url:
				if link.text in self.links.keys():
					self.links[link.text].append( 'http://www.sprucemeadows.com/tournaments/' + link.url )
		br.close()

		return True

	def download_orders(self): 
		files = []
		for i in self.links[ 'Order of Go' ]:
			#print 'downloading: ' + i 
			fileName = self.filePath + i[61:-4] + '.pdf'
			if not os.path.isfile( fileName ):
				print 'File not found, downloading now'
				urllib.urlretrieve( i, fileName )
			files.append(fileName)
		return files

	def download_results(self):
		for i in self.links[ 'Results' ]:
			print 'downloading: ' + i 
			urllib.urlretrieve( i, 'Results/Results_Class_' + i[61:-4] + '.pdf' )

def main():
	downloader = PDF_Downloader()

	print downloader.gen_tournament_link( 29, datetime.datetime.strptime( '2013 09 05', '%Y %m %d'))

	print downloader.get_PDF_links()

	for i in downloader.links['Order of Go']:
		print i

	downloader.download_orders()


# if __name__ == "__main__":
# 	main()