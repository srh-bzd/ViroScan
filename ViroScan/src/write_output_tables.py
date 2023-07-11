#!/usr/bin/python3


import argparse, json, re, sys

"""
USAGE
    ./write_output_tables.py [-h] <sample> <json_file> <output_file> <threshold> [-c <output_counts>]
DESCRIPTION
    write_output_tables.py is a script to calculate % mapped reads against each references
    according to the breseq file summary.json and return a table.
PREREQUISITE
    - python3
INFO
    This script is a part of ViroScan
AUTHOR :
    Sarah BOUZIDI
    Engineer in bioinformatics
    Centre National de la Recherche Scientifique (CNRS)
    Team Virostyle, Laboratory MIVEGEC, IRD, Montpellier
"""


def parse_json_file(json_file, threshold):
    """
    Parse input json file, keep informations we want, calculate % mapped reads and return
    results according to a threshold into a dict
    """
    dictJsonFile = json.load(json_file)
    dictPercentMappedReadsRefs = dict()
    nbrTotInputReads = dictJsonFile["reads"]["total_reads"]
    nbrTotMappedReads = dictJsonFile["reads"]["total_aligned_reads"]
    for ref in dictJsonFile["references"]["reference"]:
        percentMappedReadsRef=round(float(dictJsonFile["references"]["reference"][ref]["num_reads_mapped_to_reference"]/nbrTotMappedReads)*100, 1)
        if (percentMappedReadsRef >= threshold):
            dictPercentMappedReadsRefs[ref]=percentMappedReadsRef
    return nbrTotInputReads, nbrTotMappedReads, dictPercentMappedReadsRefs


def natural_sort(dictPercentMappedReadsRefs):
    """
    Sort dict alphanumerically by key
    """
    dictPercentMappedReadsRefsSort = dict()
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    listKeysSort = sorted(dictPercentMappedReadsRefs, key = alphanum_key)
    for key in listKeysSort:
        dictPercentMappedReadsRefsSort[key] = dictPercentMappedReadsRefs[key]
    return dictPercentMappedReadsRefsSort


def write_results(nbrTotInputReads, nbrTotMappedReads, dictPercentMappedReadsRefsSort, output_file, output_counts, sample):
    """
    Write file with the number of reads aligned and a report table with percentage of mapped 
    reads per references according to the threshold
    """
    # Counts
    print(str(sample)+"\t"+str(nbrTotInputReads)+"\t"+str(nbrTotMappedReads), file=output_counts)
    # Table
    for ref in dictPercentMappedReadsRefsSort:
        print(str(sample)+"\t"+str(ref)+"\t"+str(dictPercentMappedReadsRefsSort[ref]), file=output_file)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="write_output_tables.py is a script to calculate % mapped reads against each reference according to the breseq file summary.json and return a table;")
    parser.add_argument('sample', help="Name of the sample;",type=str)
    parser.add_argument('json_file', help="Json file from breseq output;",type=argparse.FileType('r'))
    parser.add_argument('output_file', help="Output file were the table of percent mapped reads will be written;", type=argparse.FileType('a'))
    parser.add_argument('threshold', help="Minimum percent mapped reads to report;",type=float)
    parser.add_argument('--output_counts', '-c', required=False, help="Output log file with total count of reads aligned;", type=argparse.FileType('a'), default=sys.stdout)
    args = parser.parse_args()

    nbr_tot_input_reads, nbr_tot_mapped_reads, dict_mapped_reads_refs = parse_json_file(args.json_file,args.threshold)
    dict_mapped_reads_refs_sort = natural_sort(dict_mapped_reads_refs)
    write_results(nbr_tot_input_reads, nbr_tot_mapped_reads, dict_mapped_reads_refs_sort, args.output_file, args.output_counts, args.sample)
