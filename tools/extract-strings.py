#!/usr/bin/python
"""
This script will extract strings from a Scribus-ng file.
Strings are usually in the form of PAGEOBJECT/StoryText/ITEXT
collections of objects.

This will extract the strings in these objects, and their XPaths,
in a format that is compatible with translatewiki.

Also, it will receive the same format and be able to apply it
to the original file.
"""

import json
import argparse
import itertools
import xml.etree.ElementTree as etree
from pprint import pprint


def extract_translate_paragraphs(filename='example/example.sla'):
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(filename, parser=utf8_parser)
    return tree.findall(".//PAGEOBJECT/StoryText/..")


def extract_texts(pageobject):
    """Receives a PageObject with StoryText/ITEXT
    Extracts the texts and XPaths of the ITEXT."""
    itextenumerate = enumerate(pageobject[0].findall("ITEXT"))
    return [[i, n.attrib['CH']] for i, n in itextenumerate]


def extract_keyval(node):
    keyvals = []
    if "ANNAME" in node.attrib:
        texts = extract_texts(node)
        for text in texts:
            id = ".//PAGEOBJECT[@ANNAME='%s']/StoryText/ITEXT[%02d]" % (
                node.attrib["ANNAME"],
                text[0] + 1  # index starts at 1
            )
            keyvals.append([id, text[1]])
    return keyvals


def apply_keyval(keys,
                 filename='example/example.sla',
                 filename_out='example/example_out.sla'):
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(filename, parser=utf8_parser)
    for key, value in keys.iteritems():
        node = tree.find(key)
        pprint((key, value, node))
        node.set('CH', value)
        print(node.attrib['CH'])

    tree.write(filename_out, xml_declaration=True)


def write_keyval(keyval, filename_out='example/example.json'):
    fileout = open(filename_out, "w")
    fileout.write(json.dumps({
        "en": {k: v for k, v in ids}
    }, ensure_ascii=False, indent=2, sort_keys=True).encode('utf8'))
    fileout.close()


parser = argparse.ArgumentParser(
    description='Extracts and applies string replacements on Scribus-ng files.'
)
parser.add_argument('-e', action="append_const", const="export",
                    dest="actions", help="Export to JSON file.")
parser.add_argument('-m', action="store", dest="json_filename", type=str,
                    help="Merge JSON file.")
parser.add_argument('-o', action='store', dest='output_filename',
                    help='Output file')
parser.add_argument('scribus_filename', metavar='input_SLA', type=str,
                    help='The Scribus file to be processed')

options = parser.parse_args()

if (options.json_filename):
    options.actions = options.actions or []
    options.actions.append('merge')

if (len(options.actions) != 1):
    parser.print_help()
    exit(0)

action = options.actions[0]

if action == 'export':
    file_in = options.scribus_filename
    file_out = options.output_filename
    paragraphs = extract_translate_paragraphs(file_in)
    ids = list(itertools.chain.from_iterable(map(extract_keyval, paragraphs)))
    write_keyval(ids, file_out)

if action == 'merge':
    file_in = options.scribus_filename
    json_in = options.json_filename
    file_out = options.output_filename

    with open(json_in) as f:
        keys = json.load(f)['en']

    apply_keyval(keys, file_in, file_out)
