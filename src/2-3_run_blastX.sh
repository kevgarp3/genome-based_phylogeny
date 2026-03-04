#!/bin/bash
# BLASTx: Translation of all 6 reading frames of a nucleotide query against a protein DB.

# Declaring the main working directory (dir) and the corresponding input and output directories"
indir="results/malaria-proj/2_gene-prediction/2-2_gene-parsing/Haemoproteus_tartakovskyi"
outdir="results/malaria-proj/2_gene-prediction/2-3_blast"

#Looping over the GTF files to correct their formatting when needed and parsing them to FASTA format using the genome sequences.
infile=$(ls $(echo "${indir}/*.fna"))
outfile="${outdir}/$(basename $indir).blastx"
blastx -db SwissProt -query $infile -out $outfile -evalue 1e-5 -num_descriptions 10 -num_alignments 5 -num_threads 10