#!/usr/bin/python3 
"""
Title: parseBlast_hostContigs.py
Version: 2.0
Date: 04-Mar-2026
Author: Kevin García Prado

Description:
    This script processes a BLAST-derived file to print-out to terminal the contig names
    of a genome which contains predicted genes homologous to a specific taxonomic class.

Usage:
    '''BASH
    python parseBlast_hostContigs.py <fasta-file> <blast-results> <ncbi-taxonomy-db> <uniprot-db> <class-of-interest>
    '''

Input: A GFF-parsed FASTA file, the related BLAST output file, both NCBI Taxonomy and
       UniProt databases (.dat files) and the taxon (blast-name) of interest.

Output: FASTA-formatted sequences printed out to terminal.    


Procedure:
    Section 0: Importing the necessary modules.
    Section 1: Collecting the user-entered parameters (from the command line).
    Section 2: Retrieving the first hit of each query from the BLAST file (building
               a dictionary with pairs of accession number and query ID).
    Section 3: Retrieving scientific names from the class of interest from NCBI Taxonomy.
    Section 4: Filtering queries related to the taxon of interest based on the accession
               numbers, using UniProt database.
    Section 5: Using the corresponding query ID to parse through the GFF-parsed FASTA
               file to print out the corresponding scaffolds (or contigs, rather).

Author-defined functions: None
Non-standard modules: None
"""

######################################################################################
#%% Section 0. Importing the required libraries.
######################################################################################
import sys
from pathlib import Path

######################################################################################
#%% Section 1. Collecting the user-entered parameters (from the command line).
######################################################################################
# Declaring the dictionary keys and filling up the dictionary with the user-
# entered parameters.
files_keys = ["fasta-file", "blast-results", "ncbi-taxonomy-db", "uniprot-db", "class-of-interest"]
files_dict = {}
for i in range(5):
    # Adding the corresponding new key-value pair to files_dict.
    try:
        files_dict[files_keys[i]] = sys.argv[i+1]
        # Checking whether the file actually exists where applicable.
        if i < 4 and not Path(files_dict[files_keys[i]]).is_file():
            raise TypeError
    # Printing an error message, as applicable.
    except IndexError:
        print(files_keys[i], "was not specified. Please provide it.")
    except TypeError:
        print("Error: " + files_keys[i] + " provided does not exist: " + files_dict[files_keys[i]])

######################################################################################
#%% Section 2.  Retrieving the first hit of each query from the BLAST file.
######################################################################################
# Creating an empty dictionary.
accessNums_queries_dict = {}
# Opening the BLAST results in reading mode and...
with open(files_dict[files_keys[1]], "r") as blast_results:
    # Setting a flag to read the first query.
    waiting_hit = False
    # Checking each line in the input file:
    for line in blast_results:
        # Save the query ID whenever read.
        if line.startswith("Query= "):
            curr_query = line.rstrip().split()[-1]
        # Flagging to read the first hit next if significant query-alignments were produced.
        elif "Sequences producing significant alignments" in line:
            waiting_hit = True
        # Flagging no hit is to be read if no hits were produced by the current query.
        elif "No hits found" in line:
            waiting_hit = False
        # If applicable, saving the accession number corresponding to the first hit only.
        elif waiting_hit and line.startswith(">"):
            if "|" in line:
                hit1_accessNum = line.split("|")[1]
            else:
                hit1_accessNum = line.split()[0].split(".")[0][1:]
            
            if hit1_accessNum not in accessNums_queries_dict:
                accessNums_queries_dict[hit1_accessNum] = [curr_query]
            else:
                accessNums_queries_dict[hit1_accessNum].append(curr_query)
            waiting_hit = False

######################################################################################
#%% Section 3. Retrieving scientific names from the class of interest from NCBI Taxonomy.
######################################################################################
higher_ranks = ["superkingdom", "kingdom", "superphylum", "phylum", "subphylum", "superclass"]
sciNames = []
# Opening the NCBI-Taxonomy database in reading mode and...
with open(files_dict[files_keys[2]], "r") as taxonomy_db:
    # Setting flags to check the taxonomic class and to read the taxonomic names within
    # the taxonomic class section.
    check_class = False
    reading_taxa = False
    noRank_issue = False
    # Reading each line in the database:
    for line in taxonomy_db:
        # Flagging to check if the taxonomic class matches the one of interest.
        if line.startswith("RANK"):
            taxa_rank = line.split(":")[1].strip()
            if taxa_rank == "class":
                check_class = True
            elif taxa_rank in higher_ranks and reading_taxa:
                reading_taxa = not reading_taxa
            elif taxa_rank == "no rank" and reading_taxa:
                noRank_issue = True
        # If the taxon section of interest is being read, collect all scientific names.
        elif line.startswith("SCIENTIFIC NAME"):
            # Flagging once the taxonomic class section of interest starts and finishes.
            if check_class:
                reading_taxa = files_dict[files_keys[4]] in line.split(":")[1].strip()
                check_class = not check_class
            # Saving all scientific names in the taxonomic class section of interest.
            elif reading_taxa:
                sciName = line.rstrip().split(":")[-1][1:]
                if noRank_issue:
                    noRank_issue = False
                    reading_taxa = False
                    print("## Warning! \"RANK: no rank\" interrupted reading taxa: " + sciName + " was not read.")
                else:
                    sciNames.append(sciName)

######################################################################################
#%% Section 4. Filtering queries related to the taxon of interest based on accession
# numbers, using UniProt database.
######################################################################################
filtered_queries = []
# Opening the UniProt database in reading mode and...
with open(files_dict[files_keys[3]], "r") as uniprot_db:
    accessNum = ""
    related_taxa = []
    reading_related_taxa = False
    # Reading each line in the database:
    for line in uniprot_db:
        # If the new read line is an accession number, reset the related_taxa list and
        # save the accession number.
        if line.startswith("AC"):
            related_taxa = []
            accessNum = line.rstrip().rstrip(";").split()[-1]
        # If an OC line is being read, append the corresponding taxonomical terms if the 
        # related accession number matches what is found in the BLAST results.
        elif line.startswith("OC"):
            if accessNum and accessNum in accessNums_queries_dict:
                reading_related_taxa = True
                related_taxa.extend(line.rstrip().replace(" ", "")[2:-1].rstrip(".").split(";"))
            else:
                accessNum = ""
        # If there is no more related_taxa to be read, check if the taxonomical terms
        # were previously found in the NCBI taxonomic db.
        elif reading_related_taxa:
            reading_related_taxa = False
            if any([1 for taxon in related_taxa if taxon in sciNames]):
                filtered_queries.extend(accessNums_queries_dict[accessNum])

######################################################################################
#%% Section 5. Using the corresponding query ID to parse through the GFF-parsed FASTA
# file to print out the corresponding scaffolds (or contigs, rather).
######################################################################################
# Opening the FASTA file in reading mode and...
with open(files_dict[files_keys[0]], "r") as fasta_f:
    # Reading each line in the FASTA file:
    for line in fasta_f:
        # Check if each sequence header belongs to a filtered query and printing out the
        # scaffold (or contig, rather) to which it belongs.
        if line.startswith(">") and line.split()[0][1:] in filtered_queries:
            print(line.split()[2].split("=")[-1])