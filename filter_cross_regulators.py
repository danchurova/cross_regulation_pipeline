#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys


def main():
    cross_peaks = open(sys.argv[1])
    KD = open(sys.argv[2])
    regulators_and_targets = set()

    for index,line in enumerate(cross_peaks.readlines()):
        if index % 10000 == 0:
            sys.stderr.write(str(index)+'\n')
        chrom, peak_start, peak_stop, peak_name,_, strand, _, _, _, _, _, _, target  = line.strip().split("\t")
        regulator = peak_name.split('_')[0]
        regulators_and_targets.add((regulator,target))

    sys.stderr.write('done\n' )

    for index,line in enumerate(KD.readlines()[1:]):
        if index % 10000 == 0:
            sys.stderr.write(str(index)+'\n')
        regulator, cell, id_, target, deltaPSI, deltaPSIc, z, p, q, KDFC = line.strip().split('\t')
        if (regulator, target)  in regulators_and_targets:
            print(line.strip())






if __name__ == '__main__':
        main()
