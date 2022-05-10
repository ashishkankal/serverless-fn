from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.request import urlopen
import nbformat
from nbconvert import PDFExporter
from pypandoc.pandoc_download import download_pandoc


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        download_pandoc()

        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')

        self.end_headers()

        url = 'https://jakevdp.github.io/downloads/notebooks/XKCD_plots.ipynb'
        response = urlopen(url).read().decode()
        jake_notebook = nbformat.reads(response, as_version=4)
        # print(jake_notebook)
        pdf_exporter = PDFExporter()
        pdf_data,_ = pdf_exporter.from_notebook_node(jake_notebook)

        if "name" in dic:
            message = "Hello, " + dic["name"] + "!"
        else:
            message = "Hello, stranger!"
        self.wfile.write(pdf_data)
        return
