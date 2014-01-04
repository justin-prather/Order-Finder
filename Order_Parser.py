from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTFigure, LTTextLine
from pdfminer.converter import PDFPageAggregator
import sys
from StringIO import StringIO

class Order_Parser():

	def __init__(self, filePath):
		self.filePath = filePath
		self.text_content = []
		self.content_ordered = False
		self.info = { 'Rider':[], 'Horse':[], 'Date_Time':str(), 'Class':'', 'Ring_Table':str() }

	def Parse_PDF(self):

		def parse_lt_objs (lt_objs, page_number, text=[]):
			"""Iterate through the list of LT* objects and capture the text or image data contained in each"""
			text_content = [] 
			page_text = {}
			for lt_obj in lt_objs:
				
				if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
				# text, so arrange is logically based on its column width
					text_content.append(lt_obj.get_text())

				elif isinstance(lt_obj, LTFigure):
					# LTFigure objects are containers for other LT* objects, so recurse through the children
					text_content.append(parse_lt_objs(lt_obj, page_number, text_content))

			for k, v in sorted([(key,value) for (key,value) in page_text.items()]):
				# sort the page_text hash by the keys (x0,x1 values of the bbox),
				# which produces a top-down, left-to-right sequence of related columns
				text_content.append(''.join(v))

			return '\n'.join(text_content)

		fp = open( self.filePath, 'rb')

		parser = PDFParser(fp)

		document = PDFDocument(parser)

		document.initialize('')

		rsrcmgr = PDFResourceManager()

		device = PDFPageAggregator(rsrcmgr, laparams=LAParams())

		interpreter = PDFPageInterpreter(rsrcmgr, device)

		text_content = []
		i = 0

		for page in PDFPage.create_pages(document):
			interpreter.process_page(page)
			layout = device.get_result()
			self.text_content.append(parse_lt_objs(layout, (i+1)).strip())
			i += 1

		return self.text_content

	def Order_Content(self):
		
		if(self.content_ordered == False):
			prefix = [ '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.' ]
			line = StringIO(self.toString())
			active = []
			ignore = []
			skip = False
			
			line.readline()
			line.readline()

			self.info['Class'] = line.readline()

			temp = line.readline()
			if temp != "\n":
				self.info['Date_Time'] = temp
			else:
				self.info['Date_Time'] = line.readline()

			line.readline()

			self.info['Ring_Table'] = line.readline()

			line.close()

			line = StringIO(self.toString())

			for next in line:
				
				if next == '\n':
					continue
				if next == 'HORSE\n':
					active = self.info['Horse']
					skip = True
				elif next == 'RIDER (NATIONALITY)\n':
					active = self.info[ 'Rider' ]
					skip = True
				elif (next == 'Horse \n') or (next == 'Order \n') or (next == 'Horse\n') or (next == 'Order\n') or (next == '#\n') or (next == 'of\n'):
					active = ignore
					skip = False
				else:
					active.append( next )

				if skip:
					try:
						line.next()
					except StopIteration:
						break
					try:
						line.next()
					except StopIteration:
						break

			self.content_ordered = True

			Len = len(self.info.get('Rider'))
			for i in range(1, 13):
				try:
					if any( num in self.info['Rider'][Len - i] for num in prefix ):
						self.info['Rider'].pop( Len - i )
				except IndexError:
					pass

			Len = len(self.info.get('Horse'))
			for i in range(1, 13):
				try:
					if any( num in self.info['Horse'][Len - i] for num in prefix ):
						self.info['Horse'].pop( Len - i )
				except IndexError:
					pass
			

		return self.info

	def toString(self):
		temp = ''
		for s in self.text_content:
			if not s == '\n':
				temp += s
		return temp

	def get_order_by_rider(self, rider_name):
		orders = []
		temp = ''

		rider_name_lower = rider_name.lower()

		for index in range(0, len(self.info.get('Rider'))-1):
			if rider_name_lower in self.info['Rider'][index].lower():
				orders.append(index)

		for i in orders:
			temp += str(i+1) + '. ' + self.info['Rider'][i][:-7] + ' on ' + self.info['Horse'][i] + '\n'

		return temp

	def get_order_by_horse(self, Horse_name):
		orders = []
		temp = ''

		Horse_name_lower = Horse_name.lower()

		for index in range(0, len(self.info.get('Horse'))-1):
			if Horse_name_lower in self.info['Horse'][index].lower():
				orders.append(index)

		for i in orders:
			temp += str(i+1) + '. ' + self.info['Rider'][i][:-7] + ' on ' +  self.info['Horse'][i] + '\n'

		return temp


def main():

	Order = Order_Parser( 'Sample Orders/order of go1.pdf')
	text = Order.Parse_PDF()

	info = Order.Order_Content()

	print Order.info.get('Class')
	print Order.info.get('Date_Time')
	print Order.info.get('Ring_Table')

	print Order.get_order_by_horse('Destino')
	# for i in Order.info.get('Rider'):
	# 	print i

	# for i in Order.info.get('Horse'):
	# 	print i


# if __name__ == '__main__':
# 	main()
