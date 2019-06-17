#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys


def main():
    reactive_exons = open(sys.argv[1])
    cross_peaks = open(sys.argv[2])
    regulator_target_exon = set()

    for index,line in enumerate(reactive_exons.readlines()[1:]):
        if index % 10000 == 0:
            sys.stderr.write(str(index)+'\n')
        regulator, cell, exon, target, deltaPSI, deltaPSIc, z, p, q, KDFC = line.strip().split("\t")
        regulator_target_exon.add((regulator,target, exon))

    sys.stderr.write('done\n' )

    for index,line in enumerate(cross_peaks.readlines()):
        if index % 10000 == 0:
            sys.stderr.write(str(index)+'\n')
        chrom, peak_start, peak_stop, regulator, _, strand, _, _, _, exon, _, _, target  = line.strip().split("\t")
        if (regulator, target, exon)  in regulator_target_exon:
            print(line.strip())

if __name__ == '__main__':
        main()
