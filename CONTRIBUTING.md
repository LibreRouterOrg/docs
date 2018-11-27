# Contributing to this repository

Contributing to this project will help more people be able to access to the documentation of the libremesh project.

## Tooling

There are two ways of setting up your environment based on the tools you use: SparkleShare or commandline Git).

### SparkleShare

It is a graphical tool to use a github repository as a remote folder.
It is easy for newcomers to the git world.
To set it up, you need to:
  - Install SparkleShare: https://www.sparkleshare.org/
  - Add SparkleShare key to your GitHub account: https://github.com/settings/ssh/new and you get the key from the tray icon, option Computer ID > Copy to Clipboard.
  - Add Synced folder via "Sync Remote Project" > "Github" > Remote Path: libremesh/lime-docs.git

It will take some time to sync.
After that, any change you do to the files in the folder will automatically sync with the remote server.

### Git

```bash
# Initialize
git clone git@github.com:libremesh/lime-docs.git
cd lime-docs

# Before each change
# from within the lime-docs directory
git pull
# modify file
git add .
git commit -m 'Adds a relevant change.' # Change the text between quotes to a description of what changed you applied
git push origin master
```

## Translating

In order to translate, we encourage to do it through the translatewiki.net platform.
It is connected to this repo, so everything translated there will be transfered to this repo.

https://translatewiki.net/wiki/Translating:LibreMesh

Once translations are updated on the repo (via git or translatewiki), the system will automatically generate the SLAs based on the language specific or main language file, and generate a PDF of it.

### Instructions

If doing it over git, you will need a github account for this.

  - Download repo if you haven't so yet (using commandline git or SparkleShare).
  - Fetch the last changes in the repo: `git pull` (Not needed in SparkleShare)
  - Edit the file you want to translate, these are the docs/Booklet\*/\*.\<lang\>.json files (like docs/Booklet-01-Networks/01.es.json).
  - Commit and push the changes.

## Layout

Doing layout is the task of reorganizing the content in a page to make it look properly. This means that paragraphs fit the page, they don't step over any image or margins, etc.
After documents are translated and merged, it can happen that the layout after translation may change.

For this you will need Scribus 1.5.4 and the fonts included in the repo installed in your system.

Once you push the layout to the github repo, the system will automatically generate the PDFs.

### Instructions

  - Download repo if you haven't so yet (using commandline git or SparkleShare).
  - Fetch the last changes in the repo: `git pull` (Not needed in SparkleShare)
  - Look for the file you want to do layout to. These are the sla files for any language but spanish (because it is the source language).
  - Do the layout of it.
  - Commit and push (if using commandline git). No need if using sparkleshare.

## Image translation/regionalization

It is relevant that images reflect the languages/cultures of the communities using the documentation.
That is why you can regionalize the images.

Images can be found in the asset-<language> directories of each boot is relevant that images reflect the languages/cultures of the communities using the documentation.
That is why you can regionalize the images.

The procedure is the same as for Layout or Translating, but with images.

## New Books

If you want to add a new book, you need to respect the structure of one directory inside docs, the sla file ending with -<lang>.sla .
Doing that, the system will automatically extract strings for translations, and generate pdfs and slas based on new languages.
