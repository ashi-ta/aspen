#!/bin/bash

if [ $# != 2 ]; then
    echo "Usage: $0 <list-file> <num-to-split>"
    echo "E.g.: $0 data/wav.list 10"
    echo "It creates the splitted files in e.g. data/split10/{1,2,3,...10}.list"
    exit 1
fi

data=$1
num_split=$2

if ! [ "${num_split}" -gt 0 ]; then
    echo "Invalid num-to-split argument ${num_split} (must be greater than 0)";
    exit 1;
fi

indir=`dirname ${data}`
outdir=${indir}/split${num_split}
mkdir -p ${outdir}

split --numeric-suffixes=1 --additional-suffix=.list -e -n l/${num_split} ${data} ${outdir}/file.

# rename
for i in `seq -w ${num_split}`; do
    nonzero=`echo $i | sed "s/^0//"`
    mv ${outdir}/file.${i}.list ${outdir}/file.${nonzero}.list
done

