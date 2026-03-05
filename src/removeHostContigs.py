"""
Title: removeHostContigs.py
Version: 1.0
Date: 04-Mar-2026
Author: Kevin García Prado

Description:
    This script processes a FASTA file to remove those sequences whose headers are present in
    an input text file (having one sequence header per row).

Usage:
    '''BASH
    python removeHostContigs.py <fasta-file> <seqHeaders-file>
    '''

Input: A FASTA file and a text file containing sequence headers (one per row) to be removed from
       the FASTA file.

Output: A FASTA file without the sequences needed to be removed, as per the input text file.

Procedure:
    Section 0: Importing the necessary modules.
    Section 1: Collecting the user-entered parameters (from the command line).
    Section 2: Retrieving all sequence headers to be removed from the input FASTA file.
    Section 3: Retrieving only sequence headers not to be removed and their corresponding
               sequences from the input FASTA file.
    Section 4: Printing out the processed sequences in FASTA format.

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
files_keys = ["fasta-file", "seqHeaders"]
files_dict = {}
for i in range(2):
    # Adding the corresponding new key-value pair to files_dict.
    try:
        files_dict[files_keys[i]] = sys.argv[i+1]
        # Checking whether the file actually exists.
        if not Path(files_dict[files_keys[i]]).is_file():
            raise TypeError
    # Printing an error message, as applicable.
    except IndexError:
        print(files_keys[i], "was not specified. Please provide it.")
    except TypeError:
        print("Error: " + files_keys[i] + " provided does not exist: " + files_dict[files_keys[i]])

######################################################################################
#%% Section 2. Retrieving all sequence headers to be removed from the input FASTA file.
######################################################################################
headers_toBe_removed = []
# Opening the text file with sequence headers in reading mode and...
with open(files_dict[files_keys[1]], "r") as seqHeaders:
    # Checking each line in the input file:
    for line in seqHeaders:
        # Saving all lines not being comments.
        if not line.startswith("#"):
            headers_toBe_removed.append(line.strip())

######################################################################################
#%% Section 3. Retrieving only seq-headers not to be removed and their corresponding
#              sequences from the input FASTA file.
######################################################################################
fasta_dict = {}
save_seq = False
header = ""
seq = ""
# Opening the text file with sequence headers in reading mode and...
with open(files_dict[files_keys[0]], "r") as fastaF:
    # Checking each line in the input file:
    for line in fastaF:
        # If the header is not needed to be removed, flag it to be saved.
        if line.startswith(">"):
            # Saving the header and sequence, if applicable.
            if save_seq and seq:
                fasta_dict[header] = seq
            header = line.strip().lstrip(">")
            save_seq = header.split()[0] not in headers_toBe_removed
            seq = ""
        # Supporting multi-line sequence, as well.
        elif save_seq:
            seq += line.strip()
    # Saving the last header and sequence, if applicable.
    if save_seq and seq:
                fasta_dict[header] = seq

######################################################################################
#%% Section 3. Printing out the processed sequences in FASTA format.
######################################################################################
for header in fasta_dict:
    print(">" + header)
    print(fasta_dict[header])