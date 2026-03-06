clean_genomes_dir="results/malaria-proj/1_clean-genomes/1-3_final-clean-genomes/"
genes_dir="results/malaria-proj/2_gene-prediction/2-2_gene-parsing/"
orthologs1="results/malaria-proj/3_ortholog-identification/3-1_proteinortho/"
orthologs2="results/malaria-proj/3_ortholog-identification/3-2_busco/"

# Looping over the genomes in the clean genomes directory directory...
#for genomeP in ${clean_genomes_dir}*; do
#    genome="$(basename $genomeP)"
#    genome="${genome%%.*}"
#    echo "Checking $genome ..."
#    genome_seq=$(grep -v "^>" $genomeP | tr -d "\n")
#    genome_size=$(echo $genome_seq | tr -d "\n" | wc -m)
#    genome_gc_num=$(echo $genome_seq | tr -d "\n" | tr -d "ATat" | wc -m)
#    genome_gc=$(echo ${genome_gc_num}/${genome_size}*100 | bc -l | cut -c1-5)
#    genes_num=$(grep "^>" $(echo "${genes_dir}/${genome}*/*.fna") | wc -l)
#    echo "Genome size (bp): ${genome_size}"
#    echo "Genomic GC content (%): ${genome_gc}"
#    echo "Number of genes: ${genes_num}"
#    echo ""
#done

# Checking how many orhologs were found with proteinortho and reviewing the paralog distribution:
ortho_num=$(cat ${orthologs1}"myproject.proteinortho.tsv" | awk -F "\t" '{print $1,$2}' | grep "^8" | wc -l)
echo ""
echo "Number of orthologs found by proteinortho: $ortho_num"
echo "Distribution of homologous genes (orthologs + paralogs):"
cat ${orthologs1}"myproject.proteinortho.tsv" | awk -F "\t" '{print $1,$2}' | grep "^8" | awk '{print $2}' | uniq -c
echo ""
