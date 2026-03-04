# README: Malaria Project

This workflow enables building phylogeny trees from multiple unannotated input genomes.

To achieve this the following steps are performed using the software in between parentheses:

1. Contamination removal
2. Gene prediction
3. Ortholog identification
4. Gene alignment
5. Building phylogeny trees

## Project's Tree Directory

```TEXT
├── README.md       # The README file for the project
├── data            # Contains raw data.
├── results         # Contains workflow-derived files, per run and stage.
│   └── malaria-proj
│       ├── 0_rawt
│       ├── 1_contamination-removal
│       ├── 2_gene-prediction
│       ├── 3_ortholog-identification
│       ├── 4_alignment
│       └── 5_phylogeny-tree
├── src             # Contains the project's code.
└── workflow        # Contains files ensuring reproducibility with ...
```
## Filters Choice

* Maximum GC content (%): 35
* Minimum scaffold length (bp): 3,000

## Links to Download Data

## Software

## Commands
