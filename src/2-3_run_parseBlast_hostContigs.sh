#!/bin/bash
# Recommended usage: nohup 2-4_run_parseBlast.sh <blast-dir> <fasta-dir> <ncbi-taxon-db> <uniprot-db> <outdir> 2> <nohup-log> 2>&1 &

# Declaring the main working directory (dir) and the corresponding input and output directories
blast_dir="results/malaria-proj/2_gene-prediction/2-3_blast"
fasta_dir="results/malaria-proj/2_gene-prediction/2-2_gene-parsing"
ncbi_taxon_db="results/malaria-proj/0_dbs/taxonomy.dat"
uniprot_db="results/malaria-proj/0_dbs/uniprot_sprot.dat"
taxon_of_interest="birds"

#Looping over the BLAST files to parse them using the parseBlast_hostContigs.py script.
for blast_fileP in ${blast_dir}/*.blast*; do
    blast_file="$(basename $blast_fileP)"
    prefix="${blast_file%%.*}"
    #Parsing the BLAST file
    echo "Identifying host contigs from BLAST file: $blast_file ..."
    python ./src/parseBlast_hostContigs.py \
        $(echo "${fasta_dir}/${prefix}*/*.fna") \
        "$blast_fileP" \
        "$ncbi_taxon_db" "$uniprot_db" \
        "$taxon_of_interest" \
        > "${blast_dir}/${prefix}.hostContigs.txt"
done