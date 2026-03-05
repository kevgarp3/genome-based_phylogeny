#!/bin/bash
# Recommended usage: nohup 2-1_predict-genes_GeneMark.sh <indir_name> <outdir_name> 2> <nohup-log> 2>&1 &

# Declaring the main working directory (dir) and the corresponding input and output directories
indir="results/malaria-proj/1_clean-genome"
outdir="results/malaria-proj/2_gene-prediction/2-1_GeneMark"
# Declaring the minimum contig length and the number of cores with which to run GeneMark.
#min_contig_length="10000"
#n_cores="10"

# Looping over the genome files in the input directory to run GeneMark on them given the decided parameters.
for genomeP in ${indir}/*; do
    genome="$(basename $genomeP)"
    echo "Running GeneMark (gmes_petap.pl) with: $genome"
    genes="${genome%%.*}.genes"
    mkdir -p ${outdir}/${genes}
    gmes_petap.pl --ES --cores 10 \
	    --min_contig 9000 \
	    --sequence "$genomeP" \
	    --work_dir "${outdir}/${genes}/" \
	    > "${outdir}/${genes}/gmes_petap.log" 2>&1
    
    # Correcting the GTF file format when needed to be used in the next step of the pipeline.
    genes_gtfP=$(echo "${outdir}/${genes}/*g*f*")
    genes_gtf="$(basename $genes_gtfP)"
    if [ $(grep -v ^# $genes_gtfP | awk -F "\t" '{print $1}' | awk '{print NF}' | sort | uniq) -gt 1 ]; then
        echo "Correcting the file format for: $genes ..."
        grep -v ^# $genes_gtfP | sed "s/ .*\tGeneMark.hmm/\tGeneMark.hmm/" > "${outdir}/${genes}.gtf"
    else
        echo "Correct file format: $genes"
        ln -sf "./${genes}/${genes_gtf}" "${outdir}/${genes}.gtf"
    fi
    echo ""
done
