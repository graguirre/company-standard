#
# Cleaning keywords from database 
# Gonzalo Aguirre <graguirre@gmail.com>
#
##
#
# Pre-process a list of company names
#

import csv
import sys,getopt
import re

def usage():
    print >> sys.stderr, "Options:"
    print >> sys.stderr, "    -h                Show help"
    print >> sys.stderr, "    -i <input_file>   Input file"
    print >> sys.stderr, "    -o <ouput_file>   Output file, standardized records"
    print >> sys.stderr, "Syntax: $ python2 preprocess.py <input-file>"
    sys.exit(1)

def main(argv):
    inputfile='' # init input file
    outputfile='' # init output file
    try:
        opts, args = getopt.getopt(argv,"hi:o:")
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt,arg in opts:
        if opt == '-h':
            usage()
            sys.exit(0)
        elif opt == '-i':
            inputfile = arg
        elif opt == '-o':
            outputfile = arg


    # input file must be defined
    if inputfile=='' or outputfile=='': 
        usage()
        sys.exit(3)

    try:
        fin = open(inputfile,'r')
    except IOError:
        print >> sys.stderr, "File "+ inputfile +" not found"
        sys.exit(2)
	
    out = csv.writer(open(outputfile,'w'),delimiter=',',quoting=csv.QUOTE_ALL)
    #records = csv.reader(fin)
	
    # exclusion list
    # suffixes
    # http://en.wikipedia.org/wiki/Types_of_business_entity
    pat_co = []
    pat_co.append(re.compile(r' (ShA|Shpk)$',re.IGNORECASE))
    pat_co.append(re.compile(r' (SA|SRL|SCS|SCpA|SocCol|SCeI|SE|SGR)$',re.IGNORECASE))# argentina
    pat_co.append(re.compile(r' (Inc|Ltd|NL|PtyLtd|Pty)$',re.IGNORECASE))
    pat_co.append(re.compile(r' (GEN|Verein|Eu|AG|GmbH|stG|GesbR|OG|KG)$',re.IGNORECASE))
    pat_co.append(re.compile(r' (ESV|VZW|SEP|VOF|CommV|CommVA|BVBA|NV|CVBA||CVOA)$',re.IGNORECASE))
    pat_co.append(re.compile(r' (dd|ad|dno|doo|kp|sp)$',re.IGNORECASE))
    pat_co.append(re.compile(r' (Ltda|SA)$',re.IGNORECASE))
    pat_co.append(re.compile(r' (SP|GP|LP|Corporation)$',re.IGNORECASE))
    pat_co.append(re.compile(r' (SpA|EIRL|SA|SGR|LTDA)$',re.IGNORECASE))
    pat_co.append(re.compile(r' (EI|EURL|FCP|SICAV|GEI|Association|SEP|SNC|SCS|SCA|SARL|SCOP|SEM|SAS)$',re.IGNORECASE))#france
    pat_co.append(re.compile(r' (eG|eV|GbR|OHG|KG|AG|PartG|KGaA|GmbH)$',re.IGNORECASE))#germany
    pat_co.append(re.compile(r' (Ss|Snc|Sas|Spa|Sapa|Srl|Scrl)$',re.IGNORECASE))#italy
    pat_co.append(re.compile(r' (SA|SAD|SL|SLL|SLNE|SC|SCra|SCoop)$',re.IGNORECASE))# spain
    pat_co.append(re.compile(r' (AB|HB|KB)$',re.IGNORECASE))# sweden
    pat_co.append(re.compile(r' (CIC|CIO|LLP|LP|Ltd|plc|)$',re.IGNORECASE))#UK
    pat_co.append(re.compile(r' (NA|LP|LLP|LLLP|LLC|LC|Ltd|Co|and Co|PLLC|Corp|Inc|PC|DBA|Corporation|Incorporated|Company|Limited)$',re.IGNORECASE))#US
    pat_pa = re.compile(r'\(.*?\)') #  parethesis
    pat_da = re.compile(r' -.*') #  dash
    pat_th = re.compile(r'^the ') #  initial the
    pat_sp = re.compile(r'\s+')  # extra space
    rep = [
            [',',''],
            ['.',''],
            ['\'',''],
           # ['-',' '],
            ['/',' '],
            ['&',' and '],
            ['univ ','univeristy '],
            [' tv',' television'],
            ]
    
    for s in fin:
	orig = s # copy original name
        for j in range(len(rep)):
            s = s.lower().replace(rep[j][0],rep[j][1])
        s = pat_pa.sub('', s)           # erase parenthesis
        s = pat_da.sub('', s)           # erase dash
        s = pat_th.sub('', s)           # erase initial 'the'
        s = pat_sp.sub(' ', s)          # erase extra space
        for j in range(len(pat_co)):    # erase company suffixes
            s = pat_co[j].sub('', s)
        s = s.split(' ')                
    
        s = s[0]+' '+' '.join(sorted(s[1:]))# sort list 
        s = pat_sp.sub(' ', s)
        out.writerow([orig.rstrip(),s])

if __name__=="__main__":
    main(sys.argv[1:])
    
