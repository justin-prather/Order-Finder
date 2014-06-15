from flask import Flask
from flask import request
from flask import render_template
from Order_Parser import Order_Parser
from Download_Orders_Results import PDF_Downloader
import sys, time
from datetime import datetime, timedelta

search_results = ''

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():

    #print request.form['riders'].split(', ')
    #print request.form['horses'].split(', ')
    
    global search_results

    search_results = ''

    Execute_Search( request.form )

    if not search_results == '':
    	return '<center> <h1>Search Results</h1>' + search_results.replace( '\n', '<br>') + '</center>'

    else:
    	return '<center> <h1>Search Results</h1> No orderes were found :( </center>'

def Execute_Search( form ):
	files = []

	downloader = PDF_Downloader()

	downloader.gen_tournament_link( form['Tournament'], datetime.strptime( str(form['date']), '%Y-%m-%d').date() )

	downloader.filePath = '/home/justin/Documents/Order-Finder/Orders/'

	downloader.get_PDF_links()

	files = downloader.download_orders()

	global search_results

	for order in files:
		# for name in get_items( RiderVar.get() ):
		# for order in files:
		Order = Order_Parser( order )
		Order.Parse_PDF()
		Order.Order_Content()
		riders = ''
		horses = ''
		# if not form['riders'] == '':
			#  for name in form['riders'].split(', '):
	            
	       #      text = ''
	       #      try:
	       #          text = Order.get_order_by_rider( name )
	       #      except IndexError:
	       #          print 'Possible error searching ' + order + ' for ' + name
	       #      # if not text == "":
	       		  # 	riders += text
	       #      #     print Order.info.get('Class')
	       #      #     print Order.info.get('Date_Time')
	       #      #     print Order.info.get('Ring_Table')
	       #      #     print riders

		if not form['horses'] == '':
			for name in form['horses'].split(', '):
				# print 'searching for: ' + name
				
				text = ''
				try:
					text = Order.get_order_by_horse( name )
				except IndexError:
					print 'Possible error searching ' + order + ' for ' + name
				if not text == "":
					horses += text
				#     print Order.info.get('Class')
				#     print Order.info.get('Date_Time')
				#     print Order.info.get('Ring_Table')
				#     print horses

		if (not horses == ''):# or (not riders == ''):
			#print search_results
			search_results += Order.info.get('Class')
			search_results += Order.info.get('Date_Time')
			search_results += Order.info.get('Ring_Table')
			search_results += horses
			#print search_results
			# search_results += riders
        	

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)






