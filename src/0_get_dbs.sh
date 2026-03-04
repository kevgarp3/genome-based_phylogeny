outdir=$1

# Define the databases' URLs
ncbi_tax_db="ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat"
swiss_prot_db="ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz"

# Get NCBI's taxonomy DB
wget -P $outdir $ncbi_tax_db
# Get SwissProt DB and decompress it:
wget -P $outdir $swiss_prot_db
gzip -d $(echo "${outdir}*sprot.dat.gz")