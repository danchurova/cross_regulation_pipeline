#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse

def main():

    parser = argparse.ArgumentParser(description='Parsing genome annotation file.gff')
    parser.add_argument("-gff", dest="filename", required=True,
                help="input file with gff human genome annotation", metavar="FILE")
    parser.add_argument("-o", "--output", help="directs the output to a name of your choice")
    args = parser.parse_args()


    for line in open(args.filename).readlines():
        if line[0] == '#':
            continue
        chrom, source, feature, start, stop, _, strand, _, annotation = line.strip().split("\t")
        # obtain genes
        if 'genes.bed' in args.output:
            if ' gene_type "protein_coding"' in annotation and  feature == 'gene':
                anno_dict = {}
                for element in list(filter(None, annotation.strip().split("; "))):
                    feat, value = element.strip().split(" ")
                    value = value.replace('"', '')
                    anno_dict[feat] = value
                with open(args.output, 'a') as output_file:
                    output_file.write('\t'.join([chrom, start, stop, anno_dict["gene_id"], '0', strand, anno_dict["gene_name"]]))
                    output_file.write('\n')
        # obtain exons
        elif 'exon_gene' in args.output:
            if ('transcript_type "protein_coding"' in annotation or 'transcript_type "nonsense_mediated_decay"' in annotation) and  feature == 'exon':
                anno_dict = {}
                for element in list(filter(None, annotation.strip().split("; "))):
                    feat, value = element.strip().split(" ")
                    value = value.replace('"', '')
                    anno_dict[feat] = value
                if anno_dict.get('tag') not in ['cds_end_NF', 'cds_start_NF']:
                    with open(args.output, 'a') as output_file:
                        output_file.write('\t'.join([chrom, '_'.join([chrom, start, stop, strand]), start, stop, strand, anno_dict['gene_name']]))
                        output_file.write('\n')
        # obtain stop_codons
        elif 'stop_codons' in args.output:
            if ('gene_type "protein_coding"' in annotation and 'transcript_type "nonsense_mediated_decay"' in annotation) and  feature == 'stop_codon':
                with open(args.output, 'a') as output_file:
                    output_file.write(line)



if __name__ == '__main__':
        main()
