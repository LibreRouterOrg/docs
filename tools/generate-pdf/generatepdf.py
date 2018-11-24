#!/usr/bin/python
"""
This script is used like this:
scribus-ng -g -ns -py generatepdf.py -- example/example.sla
Opens the sla file and exports a pdf in the same directory
as the sla, with the same name and pdf extension.
"""

import os
import sys

# start the script
if __name__ == '__main__':
    try:
        import scribus
        if scribus.haveDoc():
            filename = os.path.splitext(scribus.getDocName())[0]
            pdf = scribus.PDFfile()
            pdf.file = filename+".pdf"
            pdf.save()
    except:
        print (sys.modules[__name__].__doc__)
