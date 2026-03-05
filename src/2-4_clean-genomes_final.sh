#!/bin/bash
# Declaring the main working directory (dir) and the corresponding input and output directories
genomes_dir="results/malaria-proj/1_clean-genome"
blast_dir="results/malaria-proj/2_gene-prediction/2-3_blast"
out_genomes_dir="results/malaria-proj/2_gene-prediction/2-4_gene-prediction_final/2-4-1_clean-genome"
out_genes_dir="results/malaria-proj/2_gene-prediction/2-4_gene-prediction_final/2-4-2_GeneMark"
out_fasta_dir="results/malaria-proj/2_gene-prediction/2-4_gene-prediction_final/2-4-3_gene-parsing"

# Looping over the genome files to...
for genomeP in ${genomes_dir}/*; do
    genome="$(basename $genomeP)"
    hostContigs="${genome%%.*}.hostContigs"
    # If a text file containing the host contigs exists...
    if [ -f $(echo "${blast_dir}/${hostContigs}") ]; then
        # Filter the corresponding genome to discard the hostGenes.
        hostContigsP=$(ls $(echo "${blast_dir}/${hostContigs}"))
        echo "Cleaning: ${genome} with $(basename $hostContigsP) ..."
        #python ./src/removeHostContigs.py $genomeP $hostContigsP > "${out_genomes_dir}/${genome}"
        
        # Run GeneMark on the cleaned version of the genome.
        genes="${genome%%.*}.genes"
        out_specific_genes_dir=$(echo "${out_genes_dir}/${genes}")
        mkdir -p $out_specific_genes_dir
        gmes_petap.pl --ES --cores 10 \
	    --min_contig 9000 \
	    --sequence "${out_genomes_dir}/${genome}" \
	    --work_dir $out_specific_genes_dir \
	    > "${out_specific_genes_dir}/gmes_petap.log" 2>&1

        # Correcting the GTF file format when needed to be used in the next step of the pipeline.
        genes_gtfP=$(echo "${out_specific_genes_dir}/*g*f*")
        genes_gtf="$(basename $genes_gtfP)"
        if [ $(grep -v ^# $genes_gtfP | awk -F "\t" '{print $1}' | awk '{print NF}' | sort | uniq) -gt 1 ]; then
            echo "Correcting the file format for: $genes ..."
            grep -v ^# $genes_gtfP | sed "s/ .*\tGeneMark.hmm/\tGeneMark.hmm/" > "${out_genes_dir}/${genes}.gtf"
        else
            echo "Correct file format: $genes"
            ln -sf "./${genes}/${genes_gtf}" "${out_genes_dir}/${genes}.gtf"
        fi
        echo ""

        #Parsing to FASTA format
        echo "Parsing to FASTA format: $genes ..."
        ./src/gffParse.pl \
        -i "${out_genomes_dir}/${genome}" -g "${out_genes_dir}/${genes}.gtf" \
        -d "${out_fasta_dir}/${genes}" -p -c

    #else
        # Otherwise, create a soft link pointing to the already clean genome.
        #echo "Skipped: ${genome}"
        #sub_genomes_dir="$(basename $genomes_dir)"
        #ln -sf "../../${sub_genomes_dir}/${genome}" "${outdir}"
    fi
done