from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTFigure, LTTextLine
from pdfminer.converter import PDFPageAggregator



def parse_lt_objs (lt_objs, page_number, text=[]):
	"""Iterate through the list of LT* objects and capture the text or image data contained in each"""
	text_content = [] 
	#page_text = {}
	page_text = dict() # k=(x0, x1) of the bbox, v=list of text strings within that bbox width (physical column)
	
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


fp = open( 'Sample Orders/order of go.pdf', 'rb')

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
	text_content.append(parse_lt_objs(layout, (i+1)).strip())
	i += 1

for i in text_content:
	print i.strip()




