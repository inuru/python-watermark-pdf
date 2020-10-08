from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    watermark = 'Test'
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:w:",["ifile=","ofile=","watermark="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> -w <watermark>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('watermark.py -i <inputfile> -o <outputfile> -w <watermark>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-w", "--watermark"):
            watermark = arg

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    black50transparent = Color( 0, 0, 0, alpha=0.5)
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColor(black50transparent)
    can.setFont("Helvetica", 40)
    can.rotate(45)
    can.drawString(400, 50, watermark)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = inputfile

    # loop all pages
    with open(existing_pdf, "rb") as input_file:
        input_pdf = PdfFileReader(input_file)
        output = PdfFileWriter()

        for i in range(input_pdf.getNumPages()):
            pdf_page = input_pdf.getPage(i)
            pdf_page.mergePage(new_pdf.getPage(0))
            output.addPage(pdf_page)

        with open(outputfile, "wb") as merged_file:
            output.write(merged_file)

if __name__ == "__main__":
    main(sys.argv[1:])