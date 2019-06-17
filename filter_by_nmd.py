#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys


def main():
    NMD_KD = open(sys.argv[1])
    cross_peaks = open(sys.argv[2])
    targets = set()

    for index,line in enumerate(NMD_KD.readlines()[1:]):
        if index % 10000 == 0:
            sys.stderr.write(str(index)+'\n')
        exon_id, gene, deltaPSI_UPF1, deltaPSIc_UPF1, z_UPF1, p_UPF1, q_UPF1, deltaPSI_SMG6, deltaPSIc_SMG6, z_SMG6, p_SMG6, q_SMG6, deltaPSIc, p, q = line.strip().split("\t")
        target = gene
        if float(p) >= 1:
            targets.add((exon_id, target))

    sys.stderr.write('done\n' )

    for index,line in enumerate(cross_peaks.readlines()):
        if index % 10000 == 0:
            sys.stderr.write(str(index)+'\n')
        chrom, peak_start, peak_stop, regulator, _, strand, _,_,_, exon, _,_, target = line.strip().split('\t')
        if (exon, target)  in targets:
            print(line.strip())






if __name__ == '__main__':
        main()
