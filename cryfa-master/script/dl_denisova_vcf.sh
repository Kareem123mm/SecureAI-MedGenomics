          #######################################################
          #          Download Denisova (VCF) -- 6.3 GB          #
          #       - - - - - - - - - - - - - - - - - - - -       #
          #        Morteza Hosseini    seyedmorteza@ua.pt       #
          #        Diogo Pratas        pratas@ua.pt             #
          #        Armando J. Pinho    ap@ua.pt                 #
          #######################################################
#!/bin/bash

### Create a folder for VCF files and one for Denisova dataset
if [[ ! -d $dataset/$VCF/$DENISOVA ]]; then mkdir -p $dataset/$VCF/$DENISOVA; fi

### Download
# HGDP0456.hg19_1000g.22.mod - High quality
file="HGDP0456.hg19_1000g.22.mod"
wget $WGET_OP $DENISOVA_VCF_URL/$file.$vcf.gz;
gunzip < $file.$vcf.gz > $dataset/$VCF/$DENISOVA/DS-22.$vcf;
rm -f $file.$vcf.gz;