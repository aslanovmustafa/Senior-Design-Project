# converts the txt file into csv file with utf 8 encoding

with open('combined_corpus.txt', encoding='utf8') as infile, open('combined_corpus.csv','w', encoding='utf8') as outfile: 
    for line in infile: 
        outfile.write(line)