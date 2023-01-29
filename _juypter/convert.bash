#!/usr/bin/bash

FILE=$1
FILENAME="${FILE%.*}"
echo $FILE

jupyter nbconvert $FILE --to markdown 
echo -e '---mathjax: true\ncomments: true\n---' | cat - "$FILENAME.md" > temp && mv temp "$FILENAME.md"
mv *.md ../_posts/