#!/bin/bash
# Recommended usage: nohup 2-2_run_gffParse.sh <indir1_name> <indir2_name> <outdir_name> 2> <nohup-log> 2>&1 &

# Declaring the main working directory (dir) and the corresponding input and output directories
indir1="results/malaria-proj/1_clean-genome"
indir2="results/malaria-proj/2_gene-prediction/2-1_GeneMark"
outdir="results/malaria-proj/2_gene-prediction/2-2_gene-parsing"

#Looping over the GTF files to parse them to FASTA format using the genome sequences.
for fileP in ${indir2}/*gtf; do
    file="$(basename $fileP)"
    prefix="${file%%.*}"
    #Parsing the FASTA files
    echo "Parsing to FASTA format: $file ..."
    ./src/gffParse.pl \
        -i "${indir1}/${prefix}.genome" -g "${indir2}/${file}" \
        -d "${outdir}/${prefix}" -p -c
done
