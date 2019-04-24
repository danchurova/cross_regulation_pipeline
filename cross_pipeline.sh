#/usr/bin/env bash

rm -r data/py_anno_files
mkdir data/py_anno_files || true

rm -r data/outputs
mkdir data/outputs || true

# annotation
### since i do not understand how to get casette exons from gencode_annotation, it would be an input_data
python3 annotation.py -gff data/input_data/gencode.v19.annotation.gtf -o data/py_anno_files/genes.bed
python3 annotation.py -gff data/input_data/gencode.v19.annotation.gtf -o data/py_anno_files/exon_gene.tsv | sort -u > data/py_anno_files/exon_gene.tsv
python3 annotation.py -gff data/input_data/gencode.v19.annotation.gtf -o data/py_anno_files/stop_codons.bed | intersectBed -b stdin -a data/input_data/cassette_exons.bed -c > data/py_anno_files/stops.tsv
echo annotation is done

# RBPs KD shRNA to reactive exons
# KD      cell    id      name    deltaPSI        deltaPSIc       z       p       q       KDFC
# filter by q-value - consider delta PSI (5th and 6th colums)
awk '$1!=$4' data/input_data/shRNA/B07/*.tsv | grep chr | awk '$9>1.3' > data/outputs/reactive_exons.bed
awk '$5>0' data/outputs/reactive_exons.bed > data/outputs/reactive_exons_incr.bed
awk '$5<0' data/outputs/reactive_exons.bed > data/outputs/reactive_exons_decr.bed
echo RBPs KD is analyzed

# eCLIPs
# making +-5000 nt distances around exons and intersect with peaks
awk -v s=5000 '{print $1,$3-s, $4+s, $2,1,$5,$6}' OFS='\t' data/py_anno_files/exon_gene.tsv | bedtools intersect -a stdin -b data/input_data/peaks_merged.bed -wa -wb -s > data/outputs/exon_peaks.bed
# distances between peak and exon? CHECK and change
awk -v OFS="\t" '{if($7!=$11){d=(($9+$10)-($2+$3))/2;if(d<0){d=-d};print $4,$2,$3,$7,$11,d}}' data/outputs/exon_peaks.bed > data/outputs/exon_peaks_dist.tsv
echo eCLIPs are intersected with exons

# cross-peaks - intersection with genes
bedtools intersect -a data/input_data/peaks_merged.bed -b data/py_anno_files/genes.bed -wa -wb -s | awk '{split($4,a,"_");if(a[1]!=$17){print}}' | sort -k1,1 -k2,2n > data/outputs/cross_peaks.bed
echo peaks are merged with genes


# filtering peaks - only reactive exons
python3 filter_cross_regulators.py data/outputs/cross_peaks.bed data/outputs/reactive_exons.bed > data/outputs/filtered_cross_peaks.tsv
echo peaks are filtered by RBPs KD

# only HepG2 and q-value > 1.3
#awk '$2=="HepG2"' data/to_check/filtered_cross_deltaPSI.tsv | awk '$9>1.3' > data/outputs/HepG2_significant_cross_peaks.tsv
awk '$2=="HepG2"' data/outputs/filtered_cross_peaks.tsv | awk '$9>1.3' > data/outputs/HepG2_significant_cross_peaks.tsv
echo got significant for HepG2

# filter by NMD KD
python3 filter_by_nmd.py data/input_data/upf1xrn1_deltaPSI.tsv data/outputs/HepG2_significant_cross_peaks.tsv > data/outputs/cross_peaks_nmd.tsv
echo filtered by nmd
