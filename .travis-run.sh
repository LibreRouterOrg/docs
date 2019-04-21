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



# If JSON change, merge SLA with JSON
git diff-tree --no-commit-id --name-only -r HEAD | grep \.json$ | while read json_file
do
    if [ -f $json_file ]; then
        json_filename=$json_file
        filename="${json_filename%.*}"
        language="${filename##*.}"

        if [ "$MAIN_LANG" != "$language" ]; then
            filename="${filename%.*}" # because it has two extensions
            destiny_sla_filename=$filename.$language.sla
            if [ ! -f $destiny_sla_filename ]; then
                # First time doing it, copy resources file
                cp $filename.$MAIN_LANG.sla $destiny_sla_filename

                dest_dir=`dirname $filename`
                cp -r $dest_dir/assets-$MAIN_LANG $dest_dir/assets-$language

                sed -i "s/assets-$MAIN_LANG/assets-$language/" $destiny_sla_filename
            fi
            filedirname=`dirname $json_filename`

            docker run -t --rm -v `pwd`:/work nicopace/sla-to-translatewiki-json /work/$destiny_sla_filename -m /work/$json_filename -o /work/$destiny_sla_filename
        fi
    fi
done

# If SLA or Asset file or JSON change, generate PDF
git diff-tree --no-commit-id --name-only -r HEAD | grep \.sla$ | while read sla_file # TODO implement '.sla$\|asset\|.json$' processing
do
    if [ -f $sla_file ]; then
        filename="${sla_filename%.*}"
        language="${filename##*.}"

        if [ "$MAIN_LANG" != "$language" ]; then
            filename="${filename%.*}" # because it has two extensions
            docker run -t --rm -v `pwd`:/work nicopace/sla-to-pdf /work/$sla_file
        fi
    fi
done

env

git remote add httporigin https://${GH_TOKEN}@github.com/librerouterorg/docs.git > /dev/null 2>&1
git stash
git checkout master
git stash apply
git add .
git commit -m 'Automated updates.'
git push httporigin master
