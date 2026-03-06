fasta_dir="results/malaria-proj/2_gene-prediction/2-2_gene-parsing/"
outdir="results/malaria-proj/3_ortholog-identification/3-2_busco/"

# Looping over the directories in the fasta-containing directory...
for fastaP in ${fasta_dir}/*.faa; do
    genome="$(basename $fastaP)"
    genome="${genome%%.*}"
    busco -i "$fastaP" -o "${outdir}/${genome}" -m prot -l apicomplexa
done
