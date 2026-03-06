fasta_dir="results/malaria-proj/2_gene-prediction/2-2_gene-parsing/"
outdir="results/malaria-proj/3_ortholog-identification/3-1_proteinortho/"

# Looping over the directories in the fasta-containing directory...
for subdir in ${fasta_dir}*; do
    if [ -f $(echo "${subdir}/*.faa") ]; then
        sed -E '/^>/! s/[^XOUBZACDEFGHIKLMNPQRSTVWYxoubzacdefghiklmnpqrstvwy]//g; /^$/d' \
            $(echo "${subdir}/*.faa") > "${fasta_dir}/$(basename $subdir).faa"
    fi
done
proteinortho6.pl -cpus=50 -clean $(echo "${fasta_dir}/*.faa")
mv $(echo "myproject.*") $outdir
