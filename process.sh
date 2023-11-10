#!/bin/zsh

# run process.py on all story files in stories/, giving corresponding code files in code/ .

print "processing all txt files in stories/ to kt files in code/"

for filename in stories/*.txt
do
    print $filename "hello"
done