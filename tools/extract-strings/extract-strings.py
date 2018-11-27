#!/usr/bin/python3
"""
This script will extract strings from a Scribus-ng file.
Strings are usually in the form of PAGEOBJECT/StoryText/ITEXT
collections of objects.

This will extract the strings in these objects, and their XPaths,
in a format that is compatible with translatewiki.

Also, it will receive the same format and be able to apply it
to the original file.
"""

import io
import re
import json
import argparse
import xml.etree.ElementTree as etree


def extract_translate_paragraphs(filename='example/example.sla'):
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(filename, parser=utf8_parser)
    return filter(lambda po: len(po.findall('StoryText/ITEXT', po)) > 0,
                  tree.findall(".//PAGEOBJECT/StoryText/.."))


def extract_texts(pageobject):
    """Receives a PageObject with StoryText/ITEXT
    Extracts the texts and XPaths of the ITEXT."""
    itextenumerate = enumerate(pageobject[0].findall("ITEXT"))
    return [[i, n.attrib['CH']] for i, n in itextenumerate]


def remove_duplicate_spaces(string):
    import re
    return re.sub(' +', ' ', string).strip()


def extract_keyval(node):
    keyvals = []
    if "ANNAME" in node.attrib:
        texts = extract_texts(node)
        if len(texts) > 0:
            _, strings = zip(*texts)
            return [node.attrib["ANNAME"],
                    remove_duplicate_spaces(' '.join(strings))]
    return keyvals


def apply_keyval(keys,
                 filename='example/example.sla',
                 filename_out='example/example_out.sla'):
    utf8_parser = etree.XMLParser(encoding='utf-8')
    tree = etree.parse(filename, parser=utf8_parser)
    for key, value in keys.items():
        node = tree.find(".//PAGEOBJECT[@ANNAME='%s']/StoryText" % key)
        # remove childs
        for child in list(node):
            ltag = child.tag.lower()
            if ltag in ['itext']:
                node.remove(child)

        for line in value.split("\n")[::-1]:
            textnode = etree.Element("ITEXT")
            textnode.set('CH', line)
            node.insert(1, textnode)

    tree.write(filename_out, xml_declaration=True)


def number_paragraphs(file_in):
    used_numbers = set()
    utf8_parser = etree.XMLParser(encoding='UTF-8')
    tree = etree.parse(file_in, parser=utf8_parser)
    for i, paragraph in enumerate(tree.findall(".//PAGEOBJECT/StoryText/..")):
        if ("ANNAME" not in paragraph.attrib):
            paragraph.set("ANNAME", "paragraph")

        current_index_search = re.findall('^\d+', paragraph.attrib["ANNAME"])
        if (len(current_index_search) > 0):
            used_numbers.add(int(current_index_search[0]))
            continue  # Already has an index

        paragraph_name = paragraph.attrib["ANNAME"]
        while i in used_numbers:
            i = i + 1
        paragraph.set("ANNAME", ('%04d-' + paragraph_name) % i)
        used_numbers.add(i)

    tree.write(file_in, xml_declaration=True, encoding='UTF-8')


def write_keyval(keyval, filename_out='example/example.json'):
    with io.open(filename_out, "w", encoding='utf-8') as fileout:
        outmsg = json.dumps({
            "en": {k: v for k, v in ids}
        }, ensure_ascii=False, indent=2, sort_keys=True)
        fileout.write(outmsg)


parser = argparse.ArgumentParser(
    description='Extracts and applies string replacements on Scribus-ng files.'
)
parser.add_argument('-n', action="append_const", const="number_paragraphs",
                    dest="actions",
                    help="Add numbers to paragraphs in SLA in-place.")
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

if action == 'number_paragraphs':
    file_in = options.scribus_filename
    number_paragraphs(file_in)

if action == 'export':
    file_in = options.scribus_filename
    file_out = options.output_filename
    paragraphs = extract_translate_paragraphs(file_in)
    ids = map(extract_keyval, paragraphs)
    write_keyval(ids, file_out)

if action == 'merge':
    file_in = options.scribus_filename
    json_in = options.json_filename
    file_out = options.output_filename

    with io.open(json_in, mode="r", encoding='utf-8') as f:
        keys = json.load(f)['en']

    apply_keyval(keys, file_in, file_out)
