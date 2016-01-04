"""

CS68: Lab 0 - Creation of a python library and main program to simulate 
operations described in the Central Dogma to better understand the link between
a DNA sequence and resulting protein sequence(s).

Eric Oh and Winnie Ngo
"""

import string

#################################################

class DNA(object):

    def __init__(self,strand):
        self.strand = strand
        self.length = len(strand)

    def __str__(self):
        string = "5' "
        if self.length > 30:     
            string += self.strand[0:14] 
            string += "..."
            string += self.strand[-15:]
        else:
            string += self.strand
        string += " 3'"
        return string
 
    def __len__(self):
        return self.length

    def invert(self):
        self.strand = ''.join(reversed(self.strand))   #reverse the strand

        inverted = ''   #replace with corresponding complements
        for nucleotide in self.strand:
            if nucleotide == "A":
                inverted += "T"
            elif nucleotide == "T":
                inverted += "A"
            elif nucleotide == "G":
                inverted += "C"
            elif nucleotide == "C":
                inverted += "G"
        self.strand = inverted

    def getStrand(self):
        return self.strand

    def getSubStrand(self,start,stop):
        if stop > self.length:
            return self.strand[start:]
        elif start < 0:
            return self.strand[:stop]
        else:
            return self.strand[start:stop]
        
    def transcribe(self):

        RNA_list = []    #list of RNA objects

        stop_codons = ['TAG', 'TGA', 'TAA']
        i = 0

        while i != self.length:

            start_codon = self.strand.find("ATG", i)  #find first ATG
            if start_codon == -1:  #if no start codon, break
                break

            substrand = ''   

            #search rest of strand for stop codon by multiples of 3
            for codon in range(start_codon + 3, self.length, 3):  

            start_codon = self.strand.find("ATG", i)
            if start_codon == -1:
                break

            substrand = ''
            for codon in range(start_codon + 3, self.length, 3):
                if self.strand[codon: codon + 3] in stop_codons:
                    substrand = self.strand[start_codon + 3: codon]
                    substrand = substrand.replace('T', 'U')
                    RNA_list.append(RNA(substrand, start_codon + 3, codon - 1))
                    i = codon - 1
                    break
            
            i = start_codon + 3   #increment index to look for start codon
        
        return RNA_list


#################################################

class RNA(object):

    def __init__(self, strand, start, stop):
        self.strand = strand
        self.start = start
        self.stop = stop
        self.length = len(strand)

    def __str__(self):
        print str(self.start) + "-" + str(self.stop) + ": ",
        string = "5' "
        if self.length > 30: 
            string += self.strand[0:14] 
            string += "..."
            string += self.strand[-15:]
        else:
            string += self.strand
        string += " 3'"
        return string
 
    def __len__(self):
        return self.length

    def getStrand(self):
        return self.strand

    def translate(self, codon_table):
        protein = ''

        #in groups of 3, map codons to amino acid to create protein object
        for i in range(0, self.length, 3):
            key = self.strand[i: i + 3]
            if key in codon_table.keys(): #look up codons
                protein += codon_table[key]  #map to amino acid 

        return Protein(protein, self.start, self.stop)



#################################################

class Protein(object):

    def __init__(self, strand, start, stop):
        self.strand = strand
        self.start = start
        self.stop = stop
        self.length = len(strand)

    def __str__(self):
        print str(self.start) + "-" + str(self.stop) + ": ",
        string = ''
        if self.length > 30: 
            string += self.strand[0:14] 
            string += "..."
            string += self.strand[-15:]
        else:
            string += self.strand
        return string

    def __len__(self):
        return self.length

    def getStrand(self):
        return self.strand



