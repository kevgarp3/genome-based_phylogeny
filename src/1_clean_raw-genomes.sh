#!/bin/bash
# Declaring the main working directory (dir) and the corresponding input and output directories
indir="results/malaria-proj/0_raw"
outdir="results/malaria-proj/1_clean-genome"
# Declaring the suffix for file names of genomes which need to be cleaned.
dirty_suffix=".raw"
# Declaring the filtering thresholds: maximum gc content (%) and minimum scaffold length.
max_gc_cont="35"
min_scaff_l="3000"

# Looping over the genome files in the input directory to...
for genomeP in ${indir}/*; do
    genome=$(basename $genomeP)
    # ... only clean those which include the dirty_suffix.
    if [[ $genome =~ $dirty_suffix ]]; then
        prefix=${genome/$dirty_suffix/}
        echo "Cleaning: ${genome} ..."
        ./src/removeScaffold.py $genomeP $max_gc_cont ${outdir}/${prefix} $min_scaff_l
    # Otherwise, create a soft link pointing to the already clean genome.
    else
        echo "Skipped: ${genome}"
        sub_indir=$(basename $indir)
        ln -sf ../${sub_indir}/${genome} ${outdir}
    fi
done