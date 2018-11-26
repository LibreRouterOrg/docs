#!/bin/bash

set -x

MAIN_LANG=es

# If Pull Request merge or new commit, and change in main SLA file, extract JSON and commit it
git diff-tree --no-commit-id --name-only -r HEAD | grep \.es\.sla$ | while read sla_file
do
    if [ -f $sla_file ]; then
        filename=`basename $sla_file .sla`.json
        filedirname=`dirname $sla_file`
        docker run -t --rm -v `pwd`:/work nicopace/sla-to-translatewiki-json /work/$sla_file -e -o /work/$filedirname/$filename
    fi
done



# If JSON change, merge SLA with JSON change and generate PDF and create Pull Request
git diff-tree --no-commit-id --name-only -r HEAD | grep \.json$ | while read json_file
do
    if [ -f $json_file ]; then
        json_filename=$json_file
        filename="${json_filename%.*}"
        language="${filename##*.}"

        if [ "$MAIN_LANG" != "$language" ]; then
            filename="${filename%.*}" # because it has two extensions
            origin_sla_filename=$filename.$MAIN_LANG.sla
            destiny_sla_filename=$filename.$language.sla
            filedirname=`dirname $json_filename`

            docker run -t --rm -v `pwd`:/work nicopace/sla-to-translatewiki-json /work/$origin_sla_filename -m /work/$json_filename -o /work/$destiny_sla_filename
            docker run -t --rm -v `pwd`:/work nicopace/sla-to-pdf /work/$destiny_sla_filename
        fi
    fi
done

git remote add httporigin https://${GH_TOKEN}@github.com/libremesh/lime-docs.git > /dev/null 2>&1
git stash
git checkout master
git stash apply
git add `find docs -name *.pdf` `find docs -name *.json` `find . -name *.sla`
git commit -m 'Automated updates.'
git push httporigin master
