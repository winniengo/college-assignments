"""
Main program prompting the user for a sequence file and allowing them to work through the steps of the central dogma. 

Eric Oh and Winnie Ngo
"""
import os
from sequences import * 

def main():

    print "Welcome to the gene translator\n"
    
    #check if fasta file and codon file inputs are valid
    valid = False
    while not valid: 
        fasta_file = raw_input("Enter FASTA file name: ")
        codon_file = raw_input("Enter Codon Table file name: ")
        if os.path.exists(fasta_file) and os.path.exists(codon_file):
            valid = True
        else:
            print "File(s) does not exist.\n"
    
    #load DNA and print displays part of sequence
    DNA = load_DNA(fasta_file)
    print '\nDNA sequence of length %d successfully loaded:' % len(DNA)
    print DNA
    
    codon_table = load_codon_table(codon_file)
    RNA_list = []

    choice = -1
    while(choice != 0):
        print_menu()
        
        #check if user input to menu is valid
        valid = False
        while not valid:
            usr_input = raw_input("Enter choice: ")
            try:
                choice = int(usr_input)
                if choice < 0 or choice > 6:
                    print "Enter option between 0 and 6"
                else:
                    valid = True
            except Exception:
                print "%s is not a valid option. Try again." % usr_input
        
        print
        if choice == 1:
            print "Entire DNA sequence:"
            print DNA.getStrand()  #print raw DNA sequence

        elif choice == 2:
            print "DNA sequence successfully inverted:"
            DNA.invert()
            print DNA   #invert DNA sequence

        elif choice == 3:
            RNA_list = DNA.transcribe()  #transcribe DNA sequence
            print "%d Resulting mRNA sequences: " % len(RNA_list) 
            for RNA in RNA_list:
                print RNA

        elif choice == 4:
            if len(RNA_list) == 0:
                print "Transcribe DNA to mRNA first."
            else:
                for i in range(len(RNA_list)):
                    print "mRNA Sequence %d" % i
                    print RNA_list[i].getStrand()  #print raw RNA sequences

        elif choice == 5:
            if len(RNA_list) == 0:
                print "Transcribe DNA to mRNA first."
            else:
                print "%d Resulting protein sequences: " % len(RNA_list)
                for i in range(len(RNA_list)):
                    protein = RNA_list[i].translate(codon_table)
                    print protein  #translate RNA sequences

        elif choice == 6:
            filename = raw_input("Enter output filename: ")
            output_file = open(filename, 'w')   #create new output file
            for i in range(len(RNA_list)):
                protein = RNA_list[i].translate(codon_table)
                #write protein sequence to output file
                output_file.write(protein.getStrand() + '\n') 

            output_file.close()
            print "File output complete"

def load_DNA(filename):

    fasta = open(filename, 'r')
    fasta.readline() # don't care about first line
    
    sequence = ''
    for line in fasta.readlines():
        sequence += line[:-1]
    
    return DNA(sequence) 

def load_codon_table(filename):

    table = open(filename, 'r')
    codon_table = dict()  #create dictionary

    for row in table.readlines():
        row = row.strip().split(',') 

        for i in range(1, len(row)):
            codon_table[row[i]] = row[0]

    return codon_table # assembled as type dict() = {'CODON' = 'PROTEIN'}

def print_menu():

    print "\nOptions:"
    print "0) Exit"
    print "1) Print raw DNA sequence"
    print "2) Invert DNA sequence"
    print "3) Transcribe DNA sequence and print summary"
    print "4) Print raw RNA sequences"
    print "5) Translate RNA sequences and print summary"
    print "6) Print raw sequences to file"
    

if __name__=="__main__":
    main()
