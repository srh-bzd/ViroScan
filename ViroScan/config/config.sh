#!/bin/bash

<< COMMENT

    config.sh is a script belonging to ViroScan pipeline. This script contain the value by default of various args.

    AUTHOR :
        Sarah BOUZIDI
        Engineer in bioinformatics
        Centre National de la Recherche Scientifique (CNRS)
        Team Virostyle, Laboratory MIVEGEC, IRD, Montpellier
        
COMMENT

# Exit if a command exits with a non zero status
set -e


########################################################################################
#                                     VARIABLES
########################################################################################

# Path to the directory of scripts
export DIRSCRIPTS="$(dirname $0)"/src

# Path to the directory of data
export DIRDATA="$(dirname $0)"/data

# Path to the reference indexed
export REFINDEXED

# Path of tools used
export BOWTIE=bowtie2
export BRESEQ=breseq
export GDTOOLS=gdtools
export SAMTOOLS=samtools

# breseq parameters
export BRESEQ_OPTIONS="-p -t"

# Threshold
export THRESHOLD=5

# Threads
export THREADS=1

# Number unpaired file
export NBRUNPAIRED=2
