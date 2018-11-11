Documentation of LibreMesh and related topics.

For PDFs of the booklets, see http://docs.altermundi.net/.

For other documentation, see:
- https://libremesh.org/
- https://github.com/libremesh/lime-packages/issues/334#issuecomment-366731842
- https://lists.libremesh.org/pipermail/lime-users/
- https://github.com/libremesh/lime-packages/wiki

# Extract strings Documentation

This script will extract strings from a Scribus-ng file.
Strings are usually in the form of PAGEOBJECT/StoryText/ITEXT
collections of objects.

This will extract the strings in these objects, and their XPaths,
in a format that is compatible with translatewiki.

Also, it will receive the same format and be able to apply it
to the original file.

```
usage: extract-strings.py [-h] [-e] [-m JSON_FILENAME] [-o OUTPUT_FILENAME]
                          input_SLA

Extracts and applies string replacements on Scribus-ng files.

positional arguments:
  input_SLA           The Scribus file to be processed

optional arguments:
  -h, --help          show this help message and exit
  -e                  Export to JSON file.
  -m JSON_FILENAME    Merge JSON file.
  -o OUTPUT_FILENAME  Output file
```
