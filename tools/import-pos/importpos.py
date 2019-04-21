#!/usr/python

import json
import re
import glob
from os import walk

import polib

def download_translations():
    import subprocess
    
    langs = [
            "ar", "pt", "pt-br", "zh-hans", "zh-hant", "fr", "de",
            "it", "nb", "ru", "es", "tr", "ast", "ca", "el", "ko",
            "br", "sv", "diq", "sr-ec", "sr-el", "eu", "qqq", "da",
            "nl", "mk", "lb", "fi", "tcy", "skr-arab", "roa-tara",
            "id", "mnw", "pl", "kjp", "my"
            ] 
    
    for lid in langs:
        print lid
        subprocess.call(['wget', 'https://translatewiki.net/wiki/Special:ExportTranslations?group=libremesh&language=' + lid  + '&format=export-as-po'])

translatemap = {
        "01 1": "0004",
        "01 2a": "0022",
        "01 3a": "0005",
        "01 3b": "0000",
        "01 3c": "0000",
        "01 3d": "0001",
        "01 3e": "0037",
        "01 4a": "0002",
        "01 4b": "0003",
        "01 4c": "0006",
        "01 4d": "0029",
        "01 5a": "0004",
        "01 5b": "0007",
        "01 5c": "0008",
        "01 6a": "0004",
        "01 6b": "",
        "01 6c": "",
        "01 6d": "",
        "01 7a": "0024",
        "01 7b": "0025",
        "01 7c": "0021",
        "01 8a": "0010",
        "01 8b": "0009",
        "01 9": "0030",
        "01 10a": "0012",
        "01 10b": "0014",
        "01 11a": "0011",
        "01 11b": "0013",
        "01 12a": "0017",
        "01 12b": "0018",
        "01 13a": "0019",
        "01 13b": "[0]0031,[1:]0032",
        "01 14a": "[0]0034,[1:]0033",
        "01 14b": "[0]0036,[1:]0035",
        "01 15a": "0015",
        "01 15b": "0016",
        "01 15c": "",
        "01 15d": "0028",
        "01 16": "",
        "02 1": "",
        "02 2a": "0000",
        "02 2b": "0001",
        "02 3": "", #"[1]0005,[2]0010,[3]0016,[4]0024,[5]0029",
        "02 4a": "0005",
        "02 4b": "0004",
        "02 4c": "0002",
        "02 5a": "0007",
        "02 5b": "0006",
        "02 6a": "0003",
        "02 6b": "0008",
        "02 7a": "0010",
        "02 7b": "0009",
        "02 7c": "0011",
        "02 8a": "0012",
        "02 9a": "0013",
        "02 9b": "0014",
        "02 10a": "0016",
        "02 10b": "0015",
        "02 10c": "0017",
        "02 11a": "0018",
        "02 11b": "0019",
        "02 12a": "0021",
        "02 12b": "0022",
        "02 13a": "0024",
        "02 13b": "0023",
        "02 13c": "0025",
        "02 14a": "0029",
        "02 14b": "0028",
        "02 14c": "0027",
        "02 15a": "0030",
        "02 15b": "0033",
        "02 15c": "0031"
        }

# structure [language][book][key] = value
booktranslations = dict()

for (_, _, filenames) in walk('./files'):
    for filepo in filenames:

        language = filepo[52:].split('&')[0]

        if not language in booktranslations:
            booktranslations[language] = {
                    "01": dict(),
                    "02": dict()
                    }

        po = polib.pofile('./files/' + filepo, encoding='utf-8')
        for entry in po:
            if "limedocs" in entry.msgctxt:
                book = entry.msgctxt[9:11]
                paragraph = entry.msgctxt[19:entry.msgctxt.find(")", 19)]
                prevkey = book + " " + paragraph
                #print book, paragraph, entry.msgctxt[entry.msgctxt.find("=", 21)+3:]
                if prevkey in translatemap and translatemap[prevkey]:
                    key = translatemap[prevkey]
                    value = entry.msgstr[entry.msgstr.find("\n")+1:]
                    if entry.msgstr:
                        if key.find(']') > 0:
                            multikeys = key.split(",")

                            for singlekey in multikeys:
                                singlevalue = ""
                                lines = singlekey[1: singlekey.find("]")]
                                singlekey = singlekey[singlekey.find("]")+1:]
                                exec("singlevalue = value.split(\"\\n\")[" + lines + "]")
                                if not isinstance(singlevalue, basestring):
                                    singlevalue = "\n".join(singlevalue)

                                singlekey += "-paragraph"
                                booktranslations[language][book][singlekey] = singlevalue
                        else:
                            key += "-paragraph"
                            if key in booktranslations[language][book]:
                                booktranslations[language][book][key] += "\n" + value
                            else:
                                booktranslations[language][book][key] = value

        for language in booktranslations:
            for book in booktranslations[language]:
                        if len(booktranslations[language][book]) > 0:
                            if not language == "es":
                                with open(glob.glob("../../docs/*" + book + "*/")[0] + book + "." + language + '.json', 'w') as outfile:
                                    json.dump({language: booktranslations[language][book]}, outfile, indent=4)
