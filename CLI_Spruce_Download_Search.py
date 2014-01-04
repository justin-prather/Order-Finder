from Order_Parser import Order_Parser
from Download_Orders_Results import PDF_Downloader
import sys
import datetime

print 'Enter Tournament ID: '

ID = raw_input()

print 'Enter Date: ( YYYY MM DD ) '

date = datetime.datetime.strptime( raw_input(), '%Y %m %d' )

print 'Enter Rider Name: '

name = raw_input()

downloader = PDF_Downloader()

downloader.gen_tournament_link( int(ID), date )

downloader.get_PDF_links()

files = downloader.download_orders()

for order in files:
	text = ''
	Order = Order_Parser( order )
	Order.Parse_PDF()
	Order.Order_Content()
	text = Order.get_order_by_rider( name )
	if not text == "":
		print True
		print Order.info.get('Class')
		print Order.info.get('Date_Time')
		print Order.info.get('Ring_Table')
		print text



