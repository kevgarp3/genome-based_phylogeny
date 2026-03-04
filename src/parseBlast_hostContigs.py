#!/usr/bin/python3 
"""
Title: parseBlast_hostContigs.py
Version: 1.0
Date: 03-Mar-2026
Author: Kevin García Prado

Description:
    This script processes a BLAST-derived file to print-out to terminal the contig names
    of a genome which contains predicted genes homologous to a specific taxon.

Usage:
    '''BASH
    python parseBlast_hostContigs.py <fasta-file> <blast-results> <ncbi-taxonomy-db> <uniprot-db> <taxon_blast-name-of-interest>
    '''

Input: A GFF-parsed FASTA file, the related BLAST output file, both NCBI Taxonomy and
       UniProt databases (.dat files) and the taxon (blast-name) of interest.

Output: FASTA-formatted sequences printed out to terminal.    


Procedure:
    Section 0: Importing the necessary modules.
    Section 1: Collecting the user-entered parameters (from the command line).
    Section 2: Retrieving the first hit of each query from the BLAST file (building
               a dictionary with pairs of accession number and query ID).
    Section 3: Retrieving all scientific names of the taxon (blast name) of interest
               from the NCBI Taxonomy database.
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
files_keys = ["fasta-file", "blast-results", "ncbi-taxonomy-db", "uniprot-db", "taxon_blast-name-of-interest"]
files_dict = {}
for i in range(5):
    # Adding the corresponding new key-value pair to files_dict.
    try:
        files_dict[files_keys[i]] = sys.argv[i+1]
    # Printing an error message, if applicable.
    except IndexError:
        print(files_keys[i], "was not specified. Please provide it.")

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
            accessNums_queries_dict[hit1_accessNum] = curr_query
            waiting_hit = False

######################################################################################
#%% Section 3. Retrieving all scientific names of interest from NCBI Taxonomy.
######################################################################################
sciNames = set()
# Opening the NCBI-Taxonomy database in reading mode and...
with open(files_dict[files_keys[2]], "r") as taxonomy_db:
    # Setting a flag to start getting .
    taxon_blast_name_section = False
    # Reading each line in the database:
    for line in taxonomy_db:
        # Flagging once the taxon section of interest starts or finishes.
        if line.startswith("BLAST NAME"):
            if files_dict[files_keys[4]] in line.split(":")[1]:
                taxon_blast_name_section = True
            else:
                taxon_blast_name_section = False
        # If the taxon section of interes is being read, collect all scientific names.
        elif taxon_blast_name_section and line.startswith("SCIENTIFIC NAME"):
            sciNames.add(line.rstrip().split(":")[-1][1:])

######################################################################################
#%% Section 4. Filtering queries related to the taxon of interest based on the accession
# numbers, using UniProt database.
######################################################################################
filtered_queries = []
# Opening the UniProt database in reading mode and...
with open(files_dict[files_keys[3]], "r") as uniprot_db:
    accessNum = ""
    orgClass = []
    # Setting a flag for reading rows related to the organisms class.
    reading_orgClass = False
    # Reading each line in the database:
    for line in uniprot_db:
        # Appending the corresponding organism classes if the accession number matches
        # what is found in the BLAST results. 
        if line.startswith("OC") and accessNum in accessNums_queries_dict:
            reading_orgClass = True
            orgClass += line.rstrip().replace(" ", "")[2:-1].split(";")
        else:
            # Filtering the queries if orgClasses stopped being read and in case any of
            # them were found to be a scientific name of interest as per NCBI taxonomic db.
            if reading_orgClass:
                reading_orgClass = False
                if any([True for taxon in orgClass if taxon in sciNames]):
                    filtered_queries += accessNums_queries_dict[accessNum]
            # If the new read line happens to be a new accession number, saving it and 
            # resetting the orgClass list.
            if line.startswith("AC"):
                accessNum = line.rstrip().split()[-1][:-1]
                orgClass = []    

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