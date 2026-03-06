# README: Genome-Based Phylogeny. Malaria Project

This workflow enables building genome-based phylogeny trees using multiple unannotated input genomes.

To achieve this the following steps are performed:

1. Cleaning genomes (contamination removal): pre-cleaning the necessary genomes, performing gene-prediction on the pre-cleaned genomes using GeneMark, parsing GeneMark's results to FASTA format, detecting the host contigs via BLAST, and finally cleaning the genomes.
2. Gene prediction: running GeneMark with all (clean) genomes and parsing its results to FASTA format.
3. Orthologs identification: using proteinortho and BUSCO.
4. Orthologs alignment
5. Building phylogeny trees

## Project's Tree Directory

```TEXT
├── README.md       # The README file for the project
├── data            # Contains raw data.
│   ├── busco_downloads
│   ├── databases
│   └── genomes
│
├── results         # Contains workflow-derived files, per run and stage.
│   └── malaria-proj    # Run (specific project)
│       ├── 0_data
│       │   ├── 0-1_genomes
│       │   └── 0-2_databases
│       ├── 1_clean-genomes
│       │   ├── 1-1_pre-cleaning-genomes
│       │   ├── 1-2_gene-prediction
│       │   │   ├── 1-2-1_GeneMark
│       │   │   ├── 1-2-2_gene-parsing
│       │   │   └── 1-2-3_host-contigs-detection
│       │   └── 1-3_final-clean-genomes
│       ├── 2_gene-prediction
│       │   ├── 2-1_GeneMark
│       │   └── 2-2_gene-parsing
│       ├── 3_ortholog-identification
│       │   ├── 3-1_proteinortho
│       │   └── 3-2_busco
│       ├── 4_alignment
│       └── 5_phylogeny-tree
│
├── src             # Contains the project's code.
└── workflow        # Contains files ensuring reproducibility with ...
```

## Filters Choice

* Maximum GC content (%): 35
* Minimum scaffold length (bp): 3,000

## Links to Download Data

The databases used in this project can be downloaded by using `wget` with each of the following links:

* NCBI Taxonomy Database: ftp://ftp.ebi.ac.uk/pub/databases/taxonomy/taxonomy.dat
* SwissProt Database: ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz

## Software Dependencies

The following list presents all software dependencies (and versions) required to execute this workflow:

* python=3.12.12
* blast=2.17.0
* proteinortho=6.3.6
* busco=6.0.0
* clustalo=1.2.4
* raxml=8.2.13
* phylip=3.69.7

All the previous dependencies can be easily installed within a conda environment by running the following command:

```BASH
conda env create -f workflow/envs/genome-based_phylogeny.yaml
conda activate genome-based_phylogeny
```

(ONCE THE WORKFLOW IS IMPLEMENTED IN SNAKEMAKE!)
Alternatively, the following command should trigger the pipeline:

```BASH
snakemake -n --use-conda
```

## Commands

All source code and workflow implementation (via Snakemake) can be cloned from the following GitHub repository: [https://github.com/kevgarp3/genome-based_phylogeny](https://github.com/kevgarp3/genome-based_phylogeny)