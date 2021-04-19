#!/usr/bin/env python
# -*- coding: utf-8 -*
#Open Access API Project
import requests
import re
import datetime
import time
import csv
import os
#import codecs
import json

#Values are read in from the file keys.txt which is held in the same folder as the program
#The first line is a header, the second is a valid key for Sherpa/Romeo, the third is a valid email address used as part of the unpaywall API search
#https://v2.sherpa.ac.uk/api/

#https://unpaywall.org/products/api



try:
    script_path =  os.path.abspath(__file__)
    script_dir =  os.path.split(script_path)[0]
    rel_path =  "input_files/keys.txt"
    abs_file_path4 =  os.path.join(script_dir, rel_path)
    print(abs_file_path4)
    file = abs_file_path4 
    keyfile = open(file)
    keyfile.readline()
    sherpakey =  keyfile.readline()
 
    sherpakey = sherpakey[:-1]
    

    emailaddress =  keyfile.readline()
    
except:
    print('File "keys.txt" not found in folder input_files')
    i = input('Press any key to exit')
    quit()

#Create three folders within the same folder that the program file is stored – Input_files, Input_data and Output
#Verify input file and quit if not found
#The input file will be a single column CSV file headed 'DOI' listing all DOIs to be processed. 
#It is stored in the Input_data folder



inf = input('Enter the name of the input file: ')
infilestring = str(inf)
print(infilestring)
if '.csv' not in infilestring.lower():
    infilestring = infilestring+'.csv'

#Locate the input file and quit if it is not found

script_path =  os.path.abspath(__file__)
script_dir =  os.path.split(script_path)[0]
rel_path =  "input_data/"+infilestring
abs_file_path =  os.path.join(script_dir, rel_path)

doi_list = abs_file_path
print(doi_list)

try:
    filetest = open(doi_list)

except:
    i = ('File not found. Press any key to exit')
    quit()

#A csv file from Web of Science is now imported to provide author affiliation and funder detail. This file will have been created by 
# searching WoS for the DOIs in the input file and then exporting them as full records in Tab-delimited UTF-8 format. These are copied
# into a CSV file with an appropriately descriptive name
# This file is placed in the Input_data folder
#Do an advanced search in WoS using the format 
# DO = 10.1080/21680566.2017.1377646 OR DO = 10.1080/13573322.2017.1391085
wostry = 0
wosfound = 'n'
while wostry<3 and wosfound == 'n':

    wosname = input('Enter the name of the WoS file or press Enter to skip: ')
    
    if len(wosname)>0:
        
        wosused = 'Yes'
        wosfilestring = str(wosname)
        if '.csv' not in wosfilestring.lower():
            wosfilestring = wosfilestring+'.csv'

        script_path =  os.path.abspath(__file__)
        script_dir =  os.path.split(script_path)[0]
        rel_path =  "input_data/"+wosfilestring
        abs_file_path2 =  os.path.join(script_dir, rel_path)

        wosfile = abs_file_path2


        try:
            filetest = open(wosfile)
            wosfound = 'y'

        except:
            print("File not found") 
            
            wostry += 1
            if wostry<3:
                print('Try again')
                
            else:
                print('Too many tries')
                quit()
    else:
        wosused = 'No'
        wosfound = 'y'

#A Scopus file based on a search for the DOIs in the input file is now imported. 
#It is exported as a csv file and must include the Affiliation field. Scopus csv files
#automatically export in comma-delimited format
#Do and advanced search in Scopus using the format 
# DOI(10.1080/21680566.2017.1377646)  OR  DOI(10.1080/13573322.2017.1391085 )
#Include all funding details except Funding text which will use multiple columns and distort the output

scotry = 0
scofound = 'n'
while scotry<3 and scofound == 'n':
    scopusfilename = input('Enter the name of the Scopus file or press Enter to skip: ')
    
    if len(scopusfilename)>0:
        scopusused =  'Yes'
        scopusfilestring = str(scopusfilename)
        if '.csv' not in scopusfilestring.lower():
            scopusfilestring = str(scopusfilename)+'.csv'




        script_path =  os.path.abspath(__file__)
        script_dir =  os.path.split(script_path)[0]
        rel_path =  "input_data/"+scopusfilestring
        abs_file_path2 =  os.path.join(script_dir, rel_path)

        scofile = abs_file_path2
        
        
        try:
            filetest = open(scofile)
            scofound = 'y'

        except:
            print("File not found")
            scotry += 1
            if scotry<3:
             print('Try again')
            else:  
                print('Too many tries') 
                quit()
    else:
        scopusused = 'No'
        scofound = 'y'

# Note that it is not mandatory to enter use woS and Scopus files but a number of data elements such as local affiliation, department and WoS subject category
# will not be included in the output

# The top level address of a repository can be entered which is used to determine whether it occurs among the repositories attached to a given DOI by unpaywall

repstring = input('Repository address, eg.g researchcommons.waikato.ac.nz: ')

# The "local" institutional name is entered in Web of Science format. This is used to determine whether authors and reprint authors are affiliated to the institution.
# If necessary two version of an institutional name can be entered - 'Auckland Univ Technol' and 'AUT Univ'
# Web of Science abbreviations MUST be used. Check the WoS input file if necessary.

if wosused == 'Yes':

    instita = input('Enter the name of the institution in Web of Science format (e.g. Univ Auckland): ')
    institb = input('Enter alternative name: ')
    
else:
    instita = ''
    institb = ''

# The same procedure is used for Scopus

if scopusused == 'Yes':
    scopusinstnamea = input('Enter the name of the institution in Scopus format (e.g. University of Auckland): ')
    scopusinstnameb = input('Enter the alternative name of the institution in Scopus format: ')
    
else:
    scopusinstnamea = ''
    scopusinstnameb = ''

# A span of years is entered. Any DOI whose Crossref record falls outside this span will be rejected. If this is not required use a broad span such as 1900-2500

yearcorrect = 'n'
yearcount = 0
while yearcorrect == 'n' and yearcount<3:
   
    yearspan = input('Enter years to span in the format 2016-2018: ')
    
    if len(yearspan) != 9 or yearspan[4] != '-':
        print('Invalid entry')
        yearcount += 1
        if yearcount == 3:
            print('Too many tries')
            quit()
        else:
            print('Try again')
    else:
        yearcorrect = 'y'
startyear = int(yearspan[0:4])



endyear = int(yearspan[5:9])



#The program creates an output folder and file with date and time included in filename. All files related to this run of the program go into this folder.

nowstart = datetime.datetime.now()
now1 = str(nowstart)
now1 = now1.replace(':','-')
now1 = now1.replace(' ','-')
now1 = now1[:16]


ofile = str(inf+'_'+now1+'.csv')

#Create path to output file in output folder

script_path =  os.path.abspath(__file__)
script_dir =  os.path.split(script_path)[0]
newdir = "output/"+inf+'_'+now1
os.makedirs(newdir)

rel_path = newdir+"/"+ofile




abs_file_path3 =  os.path.join(script_dir, rel_path)


of1 = abs_file_path3


print(of1)


with open(of1, 'w', newline = '',encoding = 'utf-8-sig') as outputfile:

#Headings for output file

    headings = ['DOI','Evidence','Licence','OA Status','Title','Authors','Author count','Author count>20','WoS/Scopus Authors','Local author count from WoS/Scopus','Local authors','Corresponding author','Local reprint authors','Corresponding author is local','Journal','Year','Publisher','Is OA','Genre','OA Journal','Version','Host of best version','Green version available','Repositories','Number of repositories','In local repository','In DOAJ','ISSNs','Archive accepted manuscript','Embargo','Archive published version','Published version embargo','Sherpa/Romeo Link', 'Scopus citations', 'Crossref citations','Free text url','In WoS','In Scopus','APC charged in DOAJ','DOAJ Currency','DOAJ APC','Publisher Currency','Publisher APC','USD APC','Altmetric','Media stories','Policy documents','Tweets','Altmetric link','Funders','Crossref funders','WoS Subjects','Crossref subjects']
    writer =  csv.writer(outputfile)
    writer.writerow(headings)
    
    # An error file is created

    efile = str(inf+'_'+now1+'_errors.csv')

    rel_path = newdir+"/"+efile
    abs_file_path =  os.path.join(script_dir, rel_path)

    ef = abs_file_path

    recorderror = open(ef, 'w')

    recorderror.write('"DOI","Error"')
    recorderror.write('\n')

    #Set up the lists and counts


    #pmhlist records each instance of an item in a repository
    pmhlist = []
    #repositorylist is a complete list of repositories that is output at the end of the program run to aggregate the data from pmhlist
    repositorylist = []
    # The funderdata list captures every instance of funding in the WoS file
    funderdata = []
    # The funderlist lists every unique funder in the WoS file
    funderlist = []
    #Together funderdata and funderlist are used to aggregate the data at the end of the run
    # The subjectdata list captures every instance of a subject term in the WoS file
    subjectdata = []
    # Subjectlist lists every unique subject in the WoS file
    subjectlist = []
    # Together subjectdata and subjectlist are used to aggregate the data at the end of the run
    departmentlist = []
    #The departmentdata list captures every instance of a department term in the WoS file
    departmentdata = []
    # Departmentlist lists every unique department in the WoS file
    # Together departmentdata and departmentlist are used to aggregate the data at the end of the run
    
    didnotexecutelist = []
    #didnotexecutelist records dois that were not successfully processed 


    processedcount = 0
    #processedcount updates each time a doi is fully processed and is used to record progress
    linecount = 0
    #linecount 
    #linecount updates each time a line from the main DOI file is read. It will differ from processedcount if a line fails to execute correctly
    

    recordcount = 0
    #recordcount is the total number of DOIs in the main input file

    notfoundcount = 0
    #notfoundcount updates each time a DOI is not found in unpaywall
    

    #isoacount counts the rows for which OA status is true
    isoacount = 0

    outsiderangecount = 0
    #outsiderangecount updates each time a DOI has a year outside the specified range
    unexecutedcount = 0
    #unexecutedcount updates each time a line fails to execute correctly

    print()


    #Dictionaries created

    wosdict = dict()


    doajdict = dict()

    allapcissndict = dict()

    allapctitledict = dict()

    scopusdict = dict()

    sherpadict = dict()

    crossrefissndict = dict()

    #A list of unicode symbols ('\u...') and characters is read in used used to create a list that can be used in replacements
    unicodefilestring = 'unicodelist.csv'

    script_path =  os.path.abspath(__file__)
    script_dir =  os.path.split(script_path)[0]
    rel_path =  "input_files/"+unicodefilestring
    abs_file_path2 =  os.path.join(script_dir, rel_path)

    unicodefile = abs_file_path2

    tfile = open(unicodefile,encoding = 'utf-8')
    unicoderecords = csv.reader(tfile)
    unicodereplace = []
    for line in unicoderecords:
        outlist = []
        coded = line[0]
        uncoded = line[1]
        
        outlist.append(coded); outlist.append(uncoded)
        output = tuple(outlist)
        unicodereplace.append(output)
       

    yearprefixlist = ('"start":{"date-parts":[[','"published-print":{"date-parts":[[','"published-online":{"date-parts":[[','"created":{"date-parts":[[')
    #yearprefixlist is used to locate publication years in Crossref
   
    punctreplace = [('’','\''),('‘','\''),('“','\"'),('”','\"')]
    #The list punctreplace is used to tidy Scopus records

    #The csv file imported from Web of Science is used to create a dictionary of WoS authors, reprint authors, funders and subjects  
    if wosused  == 'Yes':

        wosdata = csv.DictReader(open(wosfile,mode = 'r', encoding = 'utf-8-sig'))
        for line in wosdata:

            
            
            wosdoi = line['DI']
            wosauthors = line['C1']
            wosauthors = wosauthors.replace('\'','')
            wosreprintauthor = line['RP']
            wosreprint = wosreprintauthor.replace('\'','')
            wosfund = line['FU']

            
            
            for i,j in unicodereplace:
                wosfund = wosfund.replace(i,j)

            wossubject = line['SC']
            wostitle = line['TI']

            wosreprintauthor = line['RP']
            wosauthors == line['C1']
            
            
            #wosauthors is the full author data from column C1 of the Web of Science full record output in the following format - 
            #[Reynolds, Andrew; Mann, Jim] Univ Otago, Dept Med, Dunedin 9016, Otago, New Zealand; [Reynolds, Andrew; Mann, Jim; Winter, Nicola; Te Morenga, Lisa] Univ Otago, Dept Human Nutr, Dunedin, Otago, New Zealand; [Reynolds, Andrew; Mann, Jim; Te Morenga, Lisa] Univ Otago, Edgar Natl Ctr Diabet & Obes Res, Dunedin, Otago, New Zealand; [Mann, Jim; Te Morenga, Lisa] Riddet Ctr Res Excellence, Dept Med, Dunedin, New Zealand; [Cummings, John H.] Univ Dundee, Sch Med, Dundee, Scotland; [Mann, Jim] Healthier Lives Natl Sci Challenge, Dunedin, New Zealand
            
        
            instit = instita
            if len(institb)>1 and institb in wosauthors:
                instit = institb
            
            #Counts the separate institutional groups
            allinstitcount = wosauthors.count('[')

            #Counts the institutional groups with the local aname
            localinstitcount = wosauthors.count(instit)
            
            #Finds the first occurrence of the local institute
            institposition = wosauthors.find(instit)
                 
            #woslocalauthorlist stores unique local authors
            woslocalauthorlist = []
            
            nextleftbracketfind = 0
            
            localiteration = 0
            
            authorsarelocal = 'y'
           

            
            #Loops through to find all  occurrences of the local institute within wosauthors and extract local authors
            if localiteration<localinstitcount:
                
                rightbracketposition = 0

                

                while rightbracketposition<institposition  and authorsarelocal == 'y':

                    finalauthor = 'n'

                    leftbracketposition = wosauthors.find('[',nextleftbracketfind)
                    rightbracketposition = wosauthors.find(']',leftbracketposition)
                                        
                    woslocalauthors = wosauthors[leftbracketposition:rightbracketposition]
                    institdata = wosauthors[rightbracketposition+2:]
                    nextleftbracketfind = rightbracketposition+1
                    

                    #Test whether this is the local institution.
                    
                    if instit in institdata:
                        authorsarelocal = 'y'
                    else:
                        authorsarelocal = 'n'

                    if leftbracketposition == -1:
                        woslocalauthors = wosauthors[leftbracketposition:]

                    #Extract the authors names  and add to the list of local authors for this DOI

                    woslocalauthorcount = woslocalauthors.count(';')+1
                    authoriteration = 0
                    wosauthorstart = 1

                    while authoriteration<woslocalauthorcount and authorsarelocal == 'y':


                        while finalauthor == 'n':

                            if ';' in woslocalauthors:
                                
                                endauthor = woslocalauthors.find(';',wosauthorstart)
                                woslocalauthor = woslocalauthors[wosauthorstart:endauthor]
                                woslocalauthors = woslocalauthors[endauthor+1:]
                                authoriteration += 1

                            else:
                                woslocalauthor = woslocalauthors[1:len(woslocalauthors)]
                                authoriteration += 1
                                finalauthor = 'y'


                            if woslocalauthor not in woslocalauthorlist:
                                woslocalauthorlist.append(woslocalauthor)


                            institposition = wosauthors.find(instit,rightbracketposition)

                    localiteration += 1

            #Convert the local author list to a string and clean
            woslocalauthorlist = str(woslocalauthorlist)
            woslocalauthorlist = woslocalauthorlist.replace('\'','').replace('\', \'','; ').replace('\', \'','; ').replace(']','').replace('[','').replace(', \'\'','').rstrip()
            
            lengthaulist = len(woslocalauthorlist)

            #Remove the trailing semicolon from the end

            if ';' in woslocalauthorlist:
                if woslocalauthorlist[lengthaulist-3] == ';':

                    woslocalauthorlist = woslocalauthorlist[:lengthaulist-3]


                
            #Count the local authors by semicolons
            if len(woslocalauthorlist)>2:
                numberofwoslocalauthors = woslocalauthorlist.count(';')+1
            else:
                numberofwoslocalauthors = 0


            #Extract local reprint author

            #Web of Science reprint author data. 

            #Hutchinson, DAW (corresponding author), Univ Otago, Dept Phys, Dodd Walls Ctr Photon & Quantum Technol, Dunedin, New Zealand.; Hutchinson, DAW (corresponding author), Univ Oxford, Dept Phys, Clarendon Lab, Oxford OX1 3PU, England

            #Scott, CL (corresponding author), Walter & Eliza Hall Inst Med Res, 1G Royal Parade, Parkville, Vic 3052, Australia.

            #Derraik, JGB; Camp, J (corresponding author), Better Start Natl Sci Challenge, Auckland, New Zealand.; Derraik, JGB (corresponding author), Univ Auckland, Liggins Inst, Auckland, New Zealand.; Camp, J (corresponding author), Univ Otago, Sch Phys Educ & Sports, Te Koronga, Dunedin, New Zealand.

            woslocalreprintauthor = ''
            
            instit = instita
            if len(institb)>1 and institb in wosreprintauthor:
                instit = institb
            if instit in wosreprintauthor:
                
                endauthor = 0
                counter = 0
                start = 0
                startinstit = wosreprintauthor.find(instit)
                wosreprintauthorfound = 'n'
                semicolon = wosreprintauthor.find(';')
                nextsemicolon = 0
                numberofreprintwosauthors = wosreprintauthor.count(';')+1

                if startinstit<semicolon:
                    startauthor = 0
                    endauthor = wosreprintauthor.find('(')-1
                    woslocalreprintauthor = wosreprintauthor[startauthor:endauthor]
                    
                    
                   
                    wosdict[wosdoi] = (wosauthors,woslocalauthorlist,numberofwoslocalauthors,wosreprintauthor,woslocalreprintauthor,wostitle,wossubject,wosfund)  

                else:
                    while wosreprintauthorfound == 'n' and counter <= numberofreprintwosauthors :

                        nextsemicolon = wosreprintauthor.find(';',start)

                        if nextsemicolon != -1:

                            address = wosreprintauthor[semicolon+1:nextsemicolon+1]

                            start = nextsemicolon+2

                        else:

                            address = wosreprintauthor[start:]

                        if instit in address:
                            wosreprintauthorfound = 'y'
                            endauthor = address.find('(')-1
                            woslocalreprintauthor = address[:endauthor]
                                                       
                            

               
                wosdict[wosdoi] = (wosauthors,woslocalauthorlist,numberofwoslocalauthors,wosreprintauthor,woslocalreprintauthor,wostitle,wossubject,wosfund)
             
            wosdict[wosdoi] = (wosauthors,woslocalauthorlist,numberofwoslocalauthors,wosreprintauthor,woslocalreprintauthor,wostitle,wossubject,wosfund)
          
        wosdict[wosdoi] = (wosauthors,woslocalauthorlist,numberofwoslocalauthors,wosreprintauthor,woslocalreprintauthor,wostitle,wossubject,wosfund)
        


    if scopusused == 'Yes':
        

        scodata = csv.DictReader(open(scofile,mode = 'r', encoding = 'utf-8-sig'))
        
        
        for line in scodata:
            
            
            scopusdoi = line['DOI']
            scopusauthors = line['Authors']
            scopusfullauthors = line['Authors with affiliations']
            scopusreprintauthor = line['Correspondence Address']
            scopusfunders = line['Funding Details']

            
            scopusfunders = scopusfunders.replace('\n',';').replace(';;','; ').replace(u'\xa0',u' ')

            
            
            
            scopuscitations=line['Cited by']
            
           
            #for i,j in unicodereplace:
                #scopusfunders = scopusfunders.replace(i,j)
            
                   

            for i,j in punctreplace:
                scopusauthors = scopusauthors.replace(i,j)
                scopusfullauthors = scopusfullauthors.replace(i,j)
                scopusreprintauthor = scopusreprintauthor.replace(i,j)
            

            #Select first 20 Scopus authors only
            startauthor = 0
            if scopusauthors.count(',')>20:
                authorcount = 0

                while authorcount<20:
                    end = scopusauthors.find(',',startauthor)
                    authorcount += 1
                    startauthor = end+1
                scopusauthors = scopusauthors[:end]

            
            

            #Extract local authors
            scopuslocalauthors = ''
            localreprintauthor = ''
            startauthor = 0
            authorcount = 0
            scopuslocalauthorcount = 0
            numberofscopusauthors = scopusfullauthors.count(';')+1
        
            while authorcount<numberofscopusauthors:
                endauthor = scopusfullauthors.find(';',startauthor)
                thisauthor = scopusfullauthors[startauthor:endauthor]
                if scopusinstnamea in thisauthor or (scopusinstnameb in thisauthor and len(scopusinstnameb)>1):
                    firstcomma = thisauthor.find(',')
                    lastname = thisauthor[:firstcomma]
                    lastname = lastname.strip()
                    secondcomma = thisauthor.find(',',firstcomma+1)
                    initials = thisauthor[firstcomma:secondcomma]
                    localauthorname = lastname+initials
                    scopuslocalauthorcount += 1
                    if scopuslocalauthorcount == 1:
                        scopuslocalauthors = localauthorname
                    else:
                        scopuslocalauthors = scopuslocalauthors+'; '+localauthorname

                startauthor = endauthor+1
                authorcount += 1

            #Determine if corresponding author is local
            scopusreprintauthorsemi = scopusreprintauthor.find(';')
            scopusreprintauthorshort = scopusreprintauthor[:scopusreprintauthorsemi]
            if scopusreprintauthorshort in scopuslocalauthors:
                scopuslocalreprintauthor =  scopusreprintauthorshort
                
            else:
                scopuslocalreprintauthor =  ''
                
            
            #Output Scopus data to dictionary
            
            if len(scopusdoi)>1 and scopusdoi not in scopusdict:
                scopusdict[scopusdoi] = (scopusauthors,scopusreprintauthor,scopuslocalauthors,scopuslocalauthorcount,scopuslocalreprintauthor,scopusfunders,scopusfullauthors,scopuscitations)

    #print(scopusdict)
    
    #doajlist.csv is held in the Input_files folder
    #it is imported and a dictionary created
    #Download the data from https://doaj.org/csv and rename the file doajlist.csv and place in the Input_files folder
    #Note April 2018 DOAJ List downloaded from wayback machine https://web.archive.org/web/*/https://doaj.org/csv

    doajfilestring = 'doajlist2018.csv'

    script_path =  os.path.abspath(__file__)
    script_dir =  os.path.split(script_path)[0]
    rel_path =  "input_files/"+doajfilestring
    abs_file_path2 =  os.path.join(script_dir, rel_path)

    doajfile = abs_file_path2

    doajdata = csv.DictReader(open(doajfile,mode = "r", encoding = "latin-1"))
    for line in doajdata:
        issn1 = line['Journal ISSN (print version)']
        issn2 = line['Journal EISSN (online version)']
        apc_charged = line['Journal article processing charges (APCs)']
        doaj_apc = line['APC amount']
        doaj_currency = line['Currency']
        doaj_currency = doaj_currency[:3]
        if len(issn1)>0:
            doajdict[issn1] = (apc_charged,doaj_apc,doaj_currency)

        if len(issn2)>0:
            doajdict[issn2] = (apc_charged,doaj_apc,doaj_currency)


    #Function to extract funder data. Each funder for the current DOI is checked against the full list of funders and added to if not already present. Specific data on its oastatus and whether its Author accepted manuscript and Published version can be used in repositories is sent to the list of all funder data. 
    def outputfunderdata (funder):
              
        for i,j in unicodereplace:
            funder = funder.replace(i,j)
        if funder[1] != '[':

            if  '[' in funder:
                
                bracket = funder.find('[')-1
                funder = funder[:bracket]
              

            funderlength=len(funder)
            
            if funderlength%2 == 0:
                
                halffunderlength = funderlength/2
               
            
                
                firsthalf = funder[:int(halffunderlength)]
                
                secondhalf = funder[int(halffunderlength):]
                
                if firsthalf == secondhalf:
                    funder = firsthalf
                
            
            if ':' in funder:
                
                findcolon = funder.find(':')
                funder2 = funder[:findcolon]
                
                funderdata.append((funder2,oastatus,potentialaam,potentialpdf))
                if funder2 not in funderlist:
                    funderlist.append(funder2)
            
            
                
            funderdata.append((funder,oastatus,potentialaam,potentialpdf))
            
            if funder not in funderlist:
                
                funderlist.append(funder)
                
            
            

    #Function to extract subject data
    def outputsubjectdata (subject):

        if subject not in subjectlist:
            subjectlist.append(subject)
            subjectdata.append((subject,oastatus,potentialaam,potentialpdf))
        else:
            subjectdata.append((subject,oastatus,potentialaam,potentialpdf))

    #create exchange rates dictionary
    findexchangerates = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    exchangeratedict = findexchangerates.json()

    #Program proceeds to process the file of DOIs
    #Count the number of records in the input file
    
    countlines = csv.reader(open(doi_list))

    #Moves to first DOI and counts the total number
    next(countlines)
    for line in countlines:
        
    
        check = line[0]
        
        if len(check)>0:
            recordcount += 1
            

    print(str(recordcount)+' DOIs in file')

    allapcfilestring = 'allapcs.csv'


    #Import the file of APCs extracted from https://github.com/lmatthia/publisher-oa-portfolios and consolidated
    script_path =  os.path.abspath(__file__)
    script_dir =  os.path.split(script_path)[0]
    rel_path =  "input_files/"+allapcfilestring
    abs_file_path2 =  os.path.join(script_dir, rel_path)

    allapcfile = abs_file_path2


    allapcs = csv.DictReader(open(allapcfile))

    for line in allapcs:
        allapcissn = line['issn']
        allapctitle = line['journal_title']
        allapc = line['apc']
        allapcissndict[allapcissn] = allapc
        allapctitledict[allapctitle] = allapc
        if '- The' in allapctitle:
            if allapctitle[len(allapctitle)-5:] == '- The':
                shorttitle = allapctitle[:len(allapctitle)-6]
                longtitle = 'The '+shorttitle
                allapctitledict[shorttitle] = allapc
                allapctitledict[longtitle] = allapc

    nowstart2 = datetime.datetime.now()

    records = csv.DictReader(open(doi_list))


    for line in records:
        linecount += 1
        

        print(instita)
        
        #Reset the variables that apply to each row
        #outlist captures all the output data for each row
        outlist = []
        #counts the number of repositories for this row
        repositorycount = 0

        #Variables are cleared.
        
        doi =  '';evidence =  '';licence =  '';oastatus =  '';title =  '';allauthors =  '';numauthors = 0;authorcount =  0;morethan20authors =  '';scopusauthors =  ''
        wosorscopusauthors =  '';numberoflocalauthors =  '';localauthorlist =  '';reprintauthor =  '';localreprintauthor =  '';reprintauthorislocal =  '';journal =  ''
        year =  '';publisher =  '';isoa =  '';genre =  '';oajournal =  '';version =  '';host_type =  '';greenavailable =  '';repout =  '';doaj =  '';issn =  '';inlocalrepository = ''
        aamarchiving =  ''; aamembargo =  '';publishedarchiving =  '';publishedembargo =  '';sherpalink =  '';citations =  '';freetexturl =  '';inwos =  '';inscopus = '';apccharged =  '';doajcurrency =  '';doajprice =  '';
        publishercurrency =  '';publisherapc =  '';finalapc =  '';score =  '';msmcount =  '';policycount =  '';detail =  '';funders =  '';wossubject =  ''; woslocalreprintauthor = ''; scopuslocalreprintauthor = '';crfunderlist = '';potentialaam = '';potentialpdf = '';issn1 = '';issn2 = ''
        embargo =  ''; scopuscitations = ''; crossrefsubject = ''
        #validdoi switches to 'n' if there is a problem and stops execution of the row
        validdoi = 'y'


        #Import the DOI and remove any spaces, commas etc

        doi = line['DOI']
        doi = doi.replace(' ','')
        doi = doi.replace(',','.')
        lengthdoi = len(doi)
        lastletter = doi[lengthdoi-1:]
        if lastletter == '.':
            doi = doi[:lengthdoi-1]

        #Print and output the DOI
        print(doi)

        retrycount = 0
        done = 'n'
            

            
                
        while done == 'n' and retrycount<8:

            try:            
             
                #Set variables to check if the DOI is found in unpaywall.It is sent to search twice
                #the doi will be searched for twice by the unpaywall API before being abandonned
                unpaywallsearch = 0
                #unpaywallfound switches to 'y' when the doi is found by the unpaywall API
                unpaywallfound = 'n'

                print('Checking DOI')

                
                doisearch = requests.get('https://doi.org/api/handles/'+doi,timeout=(10,20))
                doipage = doisearch.content
                doiinfo = str(doipage)
                print('DOI checked')

                if '{"responseCode":1,' not in doiinfo:
                    
                    print('Invalid DOI!')
                    validdoi = 'n'
                   
                    recorderror.write('"'+doi+'","Invalid DOI"\n')

                    
                print('Requesting Crossref data')
                getcrossrefdata = requests.get('https://api.crossref.org/works/'+doi,timeout=(10,20))
                

                crossrefdata = str(getcrossrefdata.content)
                print('Crossref data returned')
                

                

                if 'Resource not found' not in crossrefdata:

                    #Up to 5 searches can be made if Crossref is unresponsive 
                    if 'No server is available to handle this request' in crossrefdata:
                        noserver = 'y'
                        noservercount = 0
                        while noserver == 'y' and noservercount<5:

                            print('Waiting for server...')
                            print()
                            time.sleep(60)
                            getcrossrefdata = requests.get('https://api.crossref.org/works/'+doi,timeout=(10,20))
                            crossrefdata = str(getcrossrefdata.content)
                            
                            if 'No server is available to handle this request' not in crossrefdata:
                                noserver = 'n'
                            else:
                                noservercount += 1

                    #Because Crossref may contain a variety of years of publication these are examined in turn against the start and end years entered at the beginning of program execution in the format 2015-2016. A match with any of these dates will allow execution to proceed
                    #yearprefixlist = ('"start":{"date-parts":[[','"published-print":{"date-parts":[[','"published-online":{"date-parts":[[','"created":{"date-parts":[[')
                
                    year = '0000'
                    foundyear = '0000'
                    for yearprefix in yearprefixlist:
                        
                        if yearprefix in crossrefdata:
                            beginyear = crossrefdata.find(yearprefix)+len(yearprefix)
                            foundyear = crossrefdata[beginyear:beginyear+4]
                                    
                            if int(foundyear) >= startyear and int(foundyear) <= endyear:
                                
                                year = foundyear
                    
                    #If a valid year is not found then "year" is given a value that will stop the program from processing this DOI
                    if year == '0000':
                        year = foundyear
                    
                    print(year)

                    #if int(year)  >= startyear-2 and int(year)  <= endyear+2:
                    if int(year)  >= startyear and int(year)  <= endyear:

                        while unpaywallsearch<2 and unpaywallfound == 'n':

                            print('Requesting Unpaywall data')
                            

                            #Send the DOI to the unpaywall API. 
                            unpaywallfind = 'https://api.unpaywall.org/v2/'+doi+'?email='+emailaddress
  
                            findunpaywalldata = requests.get(unpaywallfind,timeout = (10,20))

                            #Read in the output from the API search to a file called unpaywalldata.
   
                            unpaywalldata = str(findunpaywalldata.content,encoding = 'utf-8')


                            print('Unpaywall data returned')
                       

                            #Check for 404 error and increment the counter

                            if 'HTTP_status_code": 404' in unpaywalldata or '"doi":' not in unpaywalldata:

                                unpaywallsearch += 1

                                time.sleep(3)

                            #Change the status to found if it is not a 404
                            else:

                                unpaywallfound = 'y'





                        #Doublecheck on the incorrect DOIs
                        if unpaywallfound == 'n':
                            

                            try:

                                doisearch = requests.get('http://dx.doi.org/'+doi,timeout = (10,20))
                                doipage = doisearch.content
                                doiinfo = str(doipage)


                                if 'This DOI cannot be found ' in doiinfo or '404 Not Found' in doiinfo or 'error-404' in doiinfo:
                                    #doi = 'Invalid DOI!'
                                    print('Invalid DOI!')
                                    validdoi = 'n'
                                    outlist.append(doi);outlist.append('Invalid DOI')
                                    
                                else:
                                    if validdoi == 'y':
                                        outlist.append(doi);outlist.append('Not found in unpaywall')
                                    print('Not found in unpaywall')
                                    validdoi = 'n'
                                   

                                notfoundcount += 1
                            except:

                                print('Not found in unpaywall')
                                validdoi = 'n'
                                outlist.append(doi);outlist.append('Not found in unpaywall')
                                if validdoi == 'y':
                                
                                    recorderror.write('"'+doi+'","Not found in unpaywall"\n')
                                notfoundcount += 1
                                


                            if 'best_oa_location": null' in unpaywalldata:
                                doi = 'DOI found but no information!'
                                print('DOI found but no information!')
                               
                                outlist.append(doi);outlist.append('No information in unpaywall')
                                validdoi = 'n'
                                notfoundcount += 1

                            elif '"title": null,' in unpaywalldata:
                                doi = 'DOI found but no information!'
                                print('DOI found but no information!')
                                
                                outlist.append(doi);outlist.append('No information in unpaywalld')
                                validdoi = 'n'
                                notfoundcount += 1

                            


                            

                        #Continue with the input for unpaywall for valid DOIs. Information on data fields at https://unpaywall.org/data-format

                        else:

                            

                            #Extract evidence - "Used for debugging. Don’t depend on the exact contents of this for anything, because values are subject to change without warning.""
                            if '"evidence": "' not in unpaywalldata:
                                evidence = ''
                            else:
                                evidencebegin = unpaywalldata.find('"evidence": "')+13
                                evidenceend = unpaywalldata.find('"',evidencebegin)
                                evidence = unpaywalldata[evidencebegin:evidenceend]

                            if '"license": ' not in unpaywalldata or '"license": null' in unpaywalldata:
                                licence = ''
                            else:
                                licencebegin = unpaywalldata.find('"license": ')+12
                                
                                licenceend = unpaywalldata.find('"',licencebegin)
                                
                                licence = unpaywalldata[licencebegin:licenceend]
                            if 'ull,' in licence:
                                licence = ''

                            if '"oa_status": "' not in unpaywalldata:
                                oastatus = ''
                            else:
                                oastatusbegin = unpaywalldata.find('"oa_status": "')+14
                                oastatusend = unpaywalldata.find('"',oastatusbegin)
                                oastatus = unpaywalldata[oastatusbegin:oastatusend]




                            #Extract the article title
                            if '"title": null,' in unpaywalldata:
                                title = ''
                            else:

                                titlebegin = unpaywalldata.find('"title": "')+10
                                titleend = unpaywalldata.find('",',titlebegin)
                                title = unpaywalldata[titlebegin:titleend]

                                #Remove HTML and tabs from title
                                title = re.sub('<.*?>','',title)
                                title = title.replace('\"','').replace('\t','')
                                

                            
                            
                            for i,j in unicodereplace:
                                title = title.replace(i,j)
                            print(title)

                            

                            #Extract the journal name
                            journalbegin = unpaywalldata.find('journal_name": ')+16
                            statuscheck = unpaywalldata[journalbegin-2:journalbegin+4]
                            #if the resource is not a journal article this will be 'null' in which case a blank is recorded
                            if 'null' in statuscheck:
                                journal = ''
                            else:
                                journalend = unpaywalldata.find('",',journalbegin)
                                journal = unpaywalldata[journalbegin:journalend]

                            
                            for i,j in unicodereplace:
                                journal = journal.replace(i,j)
                            
                            #Extract the publisher
                            if '"publisher": "' in unpaywalldata:
                                publisherbegin = unpaywalldata.find('"publisher": "')+14
                                publisherend = unpaywalldata.find('",',publisherbegin)
                                publisher = unpaywalldata[publisherbegin:publisherend]
                                for i,j in unicodereplace:
                                    publisher = publisher.replace(i,j)
                            else:
                                publisher = ''
                            
                            

                            #Extract the open access status of the item –this will be either true or false
                            isoabegin = unpaywalldata.find('"is_oa": ')+9
                            isoaend = unpaywalldata.find(',',isoabegin)
                            isoa = unpaywalldata[isoabegin:isoaend]

                            


                            

                            #Extract the genre - "Currently the genre is identical to the Crossref-reported type of a given resource. The "journal-article" type is most common, but there are many others."
                            genrebegin = unpaywalldata.find('"genre": "')+10
                            genreend = unpaywalldata.find('",',genrebegin)
                            genre = unpaywalldata[genrebegin:genreend]

                            
                            

                            #Extract the open access status of the journal."Under construction. Included for future compatibility. Will eventually include any fully-OA publication venue, regardless of inclusion in DOAJ"
                            oajournalbegin = unpaywalldata.find('"journal_is_oa": ')+17
                            oajournalend = unpaywalldata.find(',',oajournalbegin)
                            oajournal = unpaywalldata[oajournalbegin:oajournalend]


                            

                            
                            #Sent an end point to check the version status from the first section of information about the item on unpaywall. This is the "best version" of the Open Access article
                            datastandard = unpaywalldata.find('"data_standard"')

                            #Extract the version identifier of the "best version". If the article is not OA this will be 'null'
                            if '"version": null' in unpaywalldata[:datastandard]:
                                version = 'null'
                                

                            elif '"version": "' in unpaywalldata:
                                versionbegin = unpaywalldata.find('"version": "')+12
                                versionend = unpaywalldata.find('"',versionbegin)
                                version = unpaywalldata[versionbegin:versionend]

                            
                            else:
                                version = ''


                            #Extract the "host type" of the best version – this will be either Publisher or Repository
                            if '"host_type": "' in unpaywalldata:
                                hostbegin = unpaywalldata.find('"host_type": "')+14
                                hostend = unpaywalldata.find('"',hostbegin)
                                host_type = unpaywalldata[hostbegin:hostend]

                                
                            else:
                                host_type = ''


                            #The next section captures all the repository data for this DOI. Because there may be several repositories the process loops
                            #'pmh_id": "oai' indicates an item in a repository. As there may be several of these this section of the program loops until no further repositories are found
                            
                            if '"has_repository_copy": true' in unpaywalldata:
                                greenavailable = 'Yes'
                             
                                #skip represents the start of the data after the best version. This is to avoid double counting. Unpaywalldatahold is the truncated version of the unpaywall page which excludes repository data already found
                                #skip = unpaywalldata.find('"data_standard"')
                                skip = unpaywalldata.find('"oa_location')

                                
                                
                                unpaywalldatahold = unpaywalldata[skip:]
                                

                                repstart = unpaywalldatahold.find('{')

                                
                                instancecount = unpaywalldatahold.count('"oa_date":')
                                

                                for i in range(instancecount):
                                    startrepdata = unpaywalldatahold.find('{',repstart)
                                    endrepdata = unpaywalldatahold.find('},',startrepdata)
                                    repdata = unpaywalldatahold[startrepdata:endrepdata]
                                        
                                    
                                    if '"pmh_id": "oai:' in repdata:
                                        #Extract the repository address
                                        pmhbegin = repdata.find('"pmh_id": "oai:')+15
                                        pmhend = repdata.find(':',pmhbegin)
                                        pmh = repdata[pmhbegin:pmhend]

                                        #Check for dashes in the repository address which will cause a malfunction
                                        if '/' in pmh:
                                            pmhdash = pmh.find('/')
                                            pmh = pmh[:pmhdash]

                                        if '"' in pmh:
                                            pmhquotes = pmh.find('"')
                                            pmh = pmh[:pmhquotes]
                                        

                                    elif 'semanticscholar.org' in repdata:
                                        pmh =  'semanticscholar.org'
                                   
                                    else:
                                        pmh = ''

                                    
                                    if '"version": "' in repdata:
                                        versionbegin = repdata.find('"version": "')+12
                                        versionend = repdata.find('"',versionbegin)
                                        pmhversion = repdata[versionbegin:versionend]
                                        
                                    

                                    repstart = endrepdata

                                    #Check for presence of  repository in repout which is the list that aggregates data on repositories

                                    if len(pmh)>0 and pmh not in repout:
                                        
                                        repositorycount += 1
                                        

                                        #Check for line ending to show the end of the repository name
                                        if('\\n') in pmh:
                                            pmhend = unpaywalldatahold.find('\\n',pmhbegin)-2
                                            pmh = unpaywalldatahold[pmhbegin:pmhend]

                                        #Keep to see if this repository is already in the repository list and if not add it to the list

                                        if pmh not in repositorylist and len(pmh)>0:
                                            repositorylist.append(pmh)
    
                                        #pmhlist records data for each instance of an item in a repository
                                        pmhlist.append((doi,pmh,pmhversion))
                                    
                                        #repout records all the repositories in which this item is held
                                        repout = repout+pmh+' '
                                       

                                    #Moves on to the next repository for this item. The 'evidence' tag identifies the beginning of the next repository set of repository data
                                    #next = unpaywalldatahold.find('"evidence"',pmhend+10)
                                    #next = unpaywalldatahold.find('"endpoint_id":',pmhend+14)
                                    #unpaywalldatahold = unpaywalldatahold[next:]

                            else:
                                greenavailable = 'No'

                            #In rare cases the tag "pmh_id": "oai: is not present although the item is held in a repository
                            if host_type == 'repository' and repositorycount == 0:
                                repout = 'no_repository_data'
                                repositorycount = 1

                            
                            #Check to see if the item is in the local repository entered at the beginning of program execution
                            if greenavailable == 'Yes' and repstring in repout and len(repstring)>5:
                                inlocalrepository = 'Yes'
                            else:
                                inlocalrepository = 'No'
                            
                            #Check to see if journal is in DOAJ. The responses will be TRUE or FALSE
                            doajbegin = unpaywalldata.find('"journal_is_in_doaj": ')+22
                            doajend = unpaywalldata.find(',',doajbegin)
                            doaj = unpaywalldata[doajbegin:doajend]


                            #Check for URL for OA Items
                            if '"url_for_pdf":' in unpaywalldata and '"url_for_pdf": null' not in unpaywalldata:
                                urlbegin = unpaywalldata.find('"url_for_pdf": ')+16
                                urlend = unpaywalldata.find('"',urlbegin)
                                freetexturl = unpaywalldata[urlbegin:urlend]

                            elif '"free_fulltext_url": ' in unpaywalldata:
                                urlbegin = unpaywalldata.find('"free_fulltext_url": ')+23
                                urlend = unpaywalldata.find('"',urlbegin)
                                freetexturl = unpaywalldata[urlbegin:urlend]

                            elif '"url_for_landing_page": ' in unpaywalldata:
                                urlbegin = unpaywalldata.find('"url_for_landing_page": ')+25
                                urlend = unpaywalldata.find('"',urlbegin)
                                freetexturl = unpaywalldata[urlbegin:urlend]

                            

                            else:
                                freetexturl = ''

                            #Identify ISSNs. If there is more than one they will come out as a single string using a comma to separate

                            issnlist = []
                            issnbegin = unpaywalldata.find('"journal_issns":')+18
                            if unpaywalldata[issnbegin-1:issnbegin+3] == 'null':
                                issn1 = 'null'
                                issn2 = ''
                            else:
                                issnend = unpaywalldata.find('",',issnbegin)
                                issnentry = unpaywalldata[issnbegin:issnend]

                                issn1 = issnentry[0:9]
                                
                                print(issn1)
                                
                                #If unpaywall contains only one issn Crossref journals is searched to locate a second one
                                if len(issnentry)>10:
                                    issn2 = issnentry[10:19]
                                    print(issn2)
                                    
                                else:
                                    
                                    #Create a list of the ISSNs for this journal
                                    if issn1 != 'null':
                                    
                                        if issn1 in crossrefissndict:
                                           
                                            issncrentry = crossrefissndict.get(issn1)
                                            issn2 = issncrentry
                                            
                                            if issncrentry == '':
                                                issn2 = ''

                                        else:

                                            print('Requesting Crossref journal data')
                                            issn2search = 'https://api.crossref.org/journals/'+issn1
                                            
                                            getissn2 = requests.get(issn2search,timeout = (10,20))
                                            crossrefjournaldata = str(getissn2.content)
                                            

                                            if 'Resource not found'not in crossrefjournaldata:
                                            
                                                issnstart = crossrefjournaldata.find('"ISSN":[')+8
                                                issnend = crossrefjournaldata.find(']',issnstart)
                                                allissns = crossrefjournaldata[issnstart:issnend]
                                                
                                                if ',' in allissns:
                                                    firstissn = allissns[1:10]
                                                    secondissn = allissns[13:22]
                                                    
                                                    if issn == firstissn:
                                                        issn2 = secondissn
                                                    else:
                                                        issn2 = firstissn                           
                                                      
                                            else:
                                                issn2 = ''
                                 
                                if len(issn2) == 9:
                                    crossrefissndict[issn1] = issn2 
                                    crossrefissndict[issn2] = issn1
                                elif len(issn2) == 0:
                                    crossrefissndict[issn1] = ''
                                issnlist.append(issn1)
                                if len(issn2)>1 and issn2 != issn1:
                                    
                                    issnlist.append(issn2)
                                
                            
                            #Use these ISSNs to check the DOAJ data for an APC currency and amount
                            #Set variables
                            apccharged = ''
                            doajcurrency = ''
                            doajprice = ''


                            if genre == 'journal-article':
                                #Do for each ISSN

                                for issn in issnlist:

                                    if issn in doajdict:

                                        doajentry = doajdict.get(issn)

                                        doajcurrency = doajentry[2]
                                        doajprice = doajentry[1]
                                        apccharged = doajentry[0]
                                        doaj = 'TRUE'





                            


                            if oastatus == 'gold' and doaj == 'TRUE' and apccharged == 'No':
                                oastatus = 'diamond'

                            print('oastatus =  '+oastatus)




                            #Move to Sherpa/Romeo website to gather data on the OA allowances for this journal
                            #Reset variables for this item

                            aamarchiving = ''
                            
                            #sherpasearchcount = 0

                            print(journal)
                            
                            print(issn)
                            
                            sherpafound = 'No'
                            
                            if len(issn)>6:
                                
                                
                                
                                for issn in issnlist:

                                    if sherpafound == 'No':
                                    
                                    
                                        if issn in sherpadict:
                                            
                                            sherpaentry = sherpadict.get(issn)
                                            aamarchiving = sherpaentry[0]
                                            aamembargo = sherpaentry[1]
                                            publishedarchiving = sherpaentry[2]
                                            publishedembargo = sherpaentry[3]
                                            potentialaam = sherpaentry[4]
                                            potentialpdf = sherpaentry[5]
                                            sherpalink = sherpaentry[6]
                                            
                                            sherpafound = 'Yes'
                                        
                                        else:
                                    
                                            aamarchiving = ''
                                            publishedarchiving = ''
                                            aamembargo =  ''
                                            publishedembargo =  ''
                                                   

                                            #Send ISSN request to the Sherpa/Romeo API. If the ISSN is not found then each item is output as No Information. Details of the Sherpa/Romeo API can be found at – http://www.sherpa.ac.uk/romeo/SHERPA%20RoMEO%20API%20V-2-9%202013-11-25.pdf
                                            
                                            
                                            
                                            print('Requesting Sherpa/Romeo data')

                                            sherpasearchstring1 =  'https://v2.sherpa.ac.uk/cgi/retrieve_by_id?item-type=publication&api-key='+sherpakey+'&format=Json&identifier='+issn
                                            sherpasearch = requests.get(sherpasearchstring1,timeout=(10,20))
                                            sherpaapidata =   str(sherpasearch.content)
                                            if 'https://v2.sherpa.ac.uk/id/publication/' in sherpaapidata:
                                                sherpafound = 'Yes'
                                                sherpalinkstart =  sherpaapidata.find('https://v2.sherpa.ac.uk/id/publication/')
                                                sherpalinkend =  sherpaapidata.find('"',sherpalinkstart)
                                                sherpalink =  sherpaapidata[sherpalinkstart:sherpalinkend]
                                                print(sherpalink)
                                                sherpasearch2 =  requests.get(sherpalink)
                                                sherpadata =  str(sherpasearch2.content)
                                                
                                                
                                                aamarchiving =  'No'
                                                publishedarchiving =  "No"
                                                
                                                if 'Accepted Version' in sherpadata:
                                                    

                                                    acceptedcount = sherpadata.count('Accepted Version')
                                                    
                                                    acceptedend = 0
                                                    for i in range(acceptedcount):
                                                    
                                                        acceptedstart =  sherpadata.find('Accepted Version',acceptedend)
                                                        acceptedend =  sherpadata.find('<h4>',acceptedstart)
                                                        accepteddata =  sherpadata[acceptedstart:acceptedend]
                                                        

                                                        if ('Institutional Repository' in accepteddata or 'Any Website' in accepteddata or 'Non-Commercial Repository' in accepteddata or 'Any Repository' in accepteddata) and 'Prerequisite' not in accepteddata and 'Open Access fee' not in accepteddata:
                                                              
                                                            aamarchiving =  'Yes'
                                                            acceptedinrepositorydata =  accepteddata
                                                                                                                
                                                            embargostart = acceptedinrepositorydata.find('title="Embargo"></i></span><span class="permitted-oa-icon-addendum">')+68
                                                            embargoend =  acceptedinrepositorydata.find('<',embargostart)
                                                           
                                                            aamembargo =  acceptedinrepositorydata[embargostart:embargoend]
                                                           
                                                            if 'm' in aamembargo:
                                                                aamembargo =  aamembargo.replace('m',' months')
                                                                potentialaam = 'e'
                                                            if 'None' in aamembargo:
                                                                potentialaam = 'y'

                                            else:

                                                aamarchiving =  'No data'
                                            
                                            if 'Published Version' in sherpadata:
                                            
                                                publishedcount = sherpadata.count('Published Version')
                                                
                                                publishedend = 0
                                                for i in range(publishedcount):
                                                   
                                                    publishedstart =  sherpadata.find('Published Version',publishedend)
                                                    publishedend =  sherpadata.find('<h4>',publishedstart)
                                                    publisheddata =  sherpadata[publishedstart:publishedend]

                                                    if ('Institutional Repository' in publisheddata or 'Any Website' in publisheddata or 'Non-Commercial Repository' in publisheddata or 'Any Repository' in publisheddata) and 'Prerequisite' not in publisheddata and 'Open Access fee' not in publisheddata:
                                                         
                                                        publishedarchiving =  'Yes'
                                                        publishedinrepositorydata =  publisheddata
                                                
                                                        publishedembargostart =  publishedinrepositorydata.find('"Embargo"></i></span><span class="permitted-oa-icon-addendum">')+62
                                                        publishedembargoend =  publishedinrepositorydata.find('<',publishedembargostart)
                                                        publishedembargo =  publishedinrepositorydata[publishedembargostart:publishedembargoend]

                                                        if 'm' in publishedembargo:
                                                            publishedembargo =  publishedembargo.replace('m',' months')
                                                            potentialpdf =  'e'
                                                        if 'None' in publishedembargo:
                                                            potentialpdf =  'y'
                                                        #print(publishedembargo)
                                                        
                                            else:
                                                publishedarchiving =  'No data'
                                               
                                            sherpadict[issn] = (aamarchiving, aamembargo, publishedarchiving, publishedembargo, potentialaam, potentialpdf, sherpalink)
                                         
                            else:
                                print('No issn')    

                            #Program now extracts the Web of Science data stored for this DOI

                            

                            wosauthors = ''
                            woslocalauthorlist = ''
                            numberofwoslocalauthors = ''
                            wosreprintauthor = ''
                            woslocalreprintauthor = ''
                            wostitle = ''
                            wossubject = ''
                            wosfunders = ''
                            inwos = ''

                            if wosused  == 'Yes':
                                inwos = 'No'
                                #print(wosdict)

                                if doi in wosdict:
                                    inwos = 'Yes'

                                    wosentry = wosdict.get(doi)
                                    
                                    wosauthors = wosentry[0] 
                                    woslocalauthorlist = wosentry[1]
                                    numberofwoslocalauthors = wosentry[2]
                                    wosreprintauthor = wosentry[3]
                                    woslocalreprintauthor = wosentry[4]
                                    wostitle = wosentry[5]
                                    wossubject = wosentry[6]
                                    wosfunders = wosentry[7]
                                    

                                #else:
                                    #wosauthors = ''; woslocalauthorlist = ''
                                    #numberofwoslocalauthors = ''
                                    #wosreprintauthor = ''
                                    #woslocalreprintauthor = ''
                                    #wostitle = ''
                                    #wossubject = ''
                                    #wosfunders = ''
                                    #inwos = 'No'

                                
                            #else:
                                #wosauthors = ''
                                #woslocalauthorlist = ''
                                #numberofwoslocalauthors = ''
                                #wosreprintauthor = ''
                                #woslocalreprintauthor = ''
                                #wostitle = ''
                                #wossubject = ''
                                #wosfunders = ''
                                #inwos = 'No'
                            
                            scopusauthors = ''
                            scopusfullauthors = ''
                            scopusreprintauthor = '' 
                            scopuslocalauthors = ''  
                            scopuslocalauthorcount = ''
                            scopuslocalreprintauthor = ''
                            scopusfunders = ''
                            scopuscitations = ''
                            inscopus = ''
                            
                            if scopusused == 'Yes':
                                inscopus = 'No'
                                if doi in scopusdict:
                                    inscopus = 'Yes'
                                    
                                    scopusentry = scopusdict.get(doi)
                                    #print(scopusentry)
                                    
                                    
                                    
                                    
                                    scopusauthors = scopusentry[0]  
                                    scopusreprintauthor = scopusentry[1]  
                                    scopuslocalauthors = scopusentry[2]  
                                    scopuslocalauthorcount = scopusentry[3]
                                    scopuslocalreprintauthor = scopusentry[4]
                                    scopusfunders = scopusentry[5]
                                    scopusfullauthors = scopusentry[6]
                                    scopuscitations = scopusentry[7]
                                    
                                #else:
                                    #scopusauthors = ''
                                    #scopusfullauthors = ''
                                    #scopusreprintauthor = '' 
                                    #scopuslocalauthors = ''  
                                    #scopuslocalauthorcount = ''
                                    #scopuslocalreprintauthor = ''
                                    #scopusfunders = ''
                                    #scopuscitations = ''
                                    #inscopus = 'No'
                            #else:
                                #scopusauthors = ''
                                #scopusfullauthors = ''
                                #scopusreprintauthor = '' 
                                #scopuslocalauthors = ''  
                                #scopuslocalauthorcount = ''
                                #scopuslocalreprintauthor = ''
                                #scopusfunders = ''
                                #scopuscitations = ''
                                #inscopus = 'No'
                                        

                                
                            
                            
                            
                            wosorscopusauthors = wosauthors+' '+scopusfullauthors
                            wosorscopusauthors = wosorscopusauthors[:10000]
                            
                            

                            if genre == 'journal-article':
                                isjournalarticle = 'journal-article'
                            else:
                                isjournalarticle = 'not-journal-article'
                            
                            
                            

                            if woslocalauthorlist == '':
                                
                                if scopuslocalauthors == '':
                                    
                                    localauthorlist = ''
                                else:
                                    
                                    localauthorlist = scopuslocalauthors
                                    
                            else:
                                localauthorlist = woslocalauthorlist

                            

                            if numberofwoslocalauthors == '':
                                if scopuslocalauthorcount == '':
                                    numberoflocalauthors = ''
                                else:
                                    numberoflocalauthors = scopuslocalauthorcount
                            else:
                                numberoflocalauthors = numberofwoslocalauthors

                            if wosreprintauthor == '':
                                if scopusreprintauthor == '':
                                    reprintauthor = ''
                                else:
                                    reprintauthor = scopusreprintauthor
                            else:
                                reprintauthor = wosreprintauthor

                            if woslocalreprintauthor == '':
                                if scopuslocalreprintauthor == '':
                                    localreprintauthor = ''
                                else:
                                    localreprintauthor = scopuslocalreprintauthor
                            else:
                                localreprintauthor = woslocalreprintauthor

                            
                            
                            

                            

                            funders = ''
                            
                            
                            #if len(wosfunders)>0:
                            if len(wosfunders)>0:

                                
                                

                                #funders = wosfunders
                                
                                countfunders = wosfunders.count('; ')+1
                                
                                if '"' in wosfunders:
                                    wosfunders = wosfunders.replace('"','')
                                    
                                for i,j in unicodereplace                            :
                                    wosfunders = wosfunders.replace(i,j)

                                fundercount = 0
                                start = 0
                                if countfunders == 1:
                                    funder = wosfunders

                                    
                                    outputfunderdata(funder)
                                    


                                else:


                                    while fundercount<countfunders:

                                        


                                        semicolon = wosfunders.find('; ',start)

                                        if semicolon != -1:
                                            if countfunders == 1:
                                                funder = wosfunders

                                                
                                                outputfunderdata(funder)



                                            if fundercount == 0:

                                                funder = wosfunders[start:semicolon]
                                                


                                                outputfunderdata(funder)




                                            else:

                                                funder = wosfunders[start+1:semicolon]
                                                

                                                outputfunderdata(funder)

                                            start = semicolon+1
                                            fundercount += 1

                                        else:
                                            funder = wosfunders[start+1:]

                                            

                                            outputfunderdata(funder)


                                            start = semicolon+1
                                
                                            fundercount += 1
                            
                            if len(scopusfunders)>0:

                                
                                
                                countfunders = scopusfunders.count('; ')+1
                                
                                if '"' in scopusfunders:
                                    scopusfunders = scopusfunders.replace('"','')
                                    
                                fundercount = 0
                                start = 0
                                if countfunders == 1:
                                    funder = scopusfunders

                                    
                                    outputfunderdata(funder)


                                else:


                                    while fundercount<countfunders:

                                        


                                        semicolon = scopusfunders.find('; ',start)

                                        if semicolon != -1:
                                            if countfunders == 1:
                                                funder = scopusfunders
                                                

                                                
                                                outputfunderdata(funder)




                                            if fundercount > 0:

                                                funder = scopusfunders[start+1:semicolon]
                                                
                                                

                                                
                                                
                                                outputfunderdata(funder)




                                            else:

                                                funder = scopusfunders[start:semicolon]
                                                
                                                
                                                outputfunderdata(funder)

                                            start = semicolon+1
                                            fundercount += 1

                                        else:
                                            funder = scopusfunders[start+1:]
                                            
                                            outputfunderdata(funder)


                                            start = semicolon+1
                                
                                            fundercount += 1
                                                   

                                    

                                        

                            else:
                                funders =  ''

                            
                            
                                            
                                    
                           
                            if len(wosfunders)>0 and len(scopusfunders)>0:
                                funders = wosfunders+'; '+scopusfunders
                            elif len(wosfunders)>0:
                                funders = wosfunders
                            elif len(scopusfunders)>0:
                                funders = scopusfunders
                            else:
                                funders = ''
                            
                            
                            

                            if '"' in wossubject:

                                wossubject = wossubject.replace('"','')

                            countsubjects = wossubject.count('; ')+1

                            subjectcount = 0
                            start = 0

                            if len(wossubject) == 0:
                                countsubjects = 0
                            
                            
                            

                            elif countsubjects == 1:
                                subject = wossubject



                                outputsubjectdata(subject)


                            else:



                                while subjectcount<countsubjects:



                                    semicolon = wossubject.find('; ',start)

                                    if semicolon != -1:
                                        if countsubjects == 1:
                                            subject = wossubject

                                            
                                            outputsubjectdata(subject)



                                        if subjectcount == 0:

                                            subject = wossubject[start:semicolon]


                                            outputsubjectdata(subject)
                                            




                                        else:

                                            subject = wossubject[start+1:semicolon]

                                            outputsubjectdata(subject)
                                            

                                        start = semicolon+1
                                        subjectcount += 1

                                    else:
                                        subject = wossubject[start+1:]

                                        outputsubjectdata(subject)
                                        


                                        start = semicolon+1
                                        subjectcount += 1

                            
                            
                            if instita in wosauthors:
                                numberoflocaldepts = wosauthors.count(instita)

                                
                                
                                start = 0
                                tempdepartmentlist = []
                                for i in range(0,numberoflocaldepts):
                                    department = ''
                                    startdept = wosauthors.find(instita,start)
                                    firstcomma = wosauthors.find(',',startdept)
                                    secondcomma = wosauthors.find(',',firstcomma+1)
                                    department = wosauthors[startdept:secondcomma]

                                    if len(department)>0:                    
                                        if department not in tempdepartmentlist:
                                            tempdepartmentlist.append(department)
                                        if department not in departmentlist:
                                            departmentlist.append(department)
                                    start = secondcomma
                                    

                                
                                for department in tempdepartmentlist:
                                    
                                    departmentdata.append((department,isjournalarticle,oastatus,potentialaam,potentialpdf))
                            
                            
                            if scopusinstnamea in scopusfullauthors:
                                
                                
                                tempdepartmentlist = []
                                numberofauthors = scopusfullauthors.count(';')+1
                                
                                
                                start = 0
                                startauthor = 0
                                for i in range(0,numberofauthors):
                                    
                                    department = ''
                                    endauthor = scopusfullauthors.find(';',startauthor)
                                    allauthor = scopusfullauthors[startauthor:endauthor]
                                    
                                    
                                    
                                    if scopusinstnamea in allauthor:
                                        
                                        startdepartment = allauthor.find('.,')+3
                                        
                                        enddepartment = allauthor.find(scopusinstnamea)+len(scopusinstnamea)
                                        
                                        department = allauthor[startdepartment:enddepartment]
                                        
                                                                
                                    startauthor = endauthor+1
                                    if len(department)>0:
                                        if department not in tempdepartmentlist:
                                            tempdepartmentlist.append(department)
                                        if department not in departmentlist:
                                            departmentlist.append(department)

                                    
                                    

                                for department in tempdepartmentlist:
                                    
                                    departmentdata.append((department,isjournalarticle,oastatus,potentialaam,potentialpdf))
                                    
                        
                            #Check Crossref for citations of the item identified by its DOI
                            
                            if validdoi == 'y':
                                
                                

                                if '"is-referenced-by-count":' in crossrefdata:
                                    refstart = crossrefdata.find('"is-referenced-by-count":')+25
                                    refend = crossrefdata.find(',',refstart)
                                    citations = crossrefdata[refstart:refend]
                                elif 'Resource not found' in crossrefdata:
                                    citations = ''
                                else:
                                    citations = '0'

                                if '"page":"' in crossrefdata:
                                    startpage = crossrefdata.find('"page":"')+8
                                    endpage = crossrefdata.find('"',startpage)
                                    crossrefpages = crossrefdata[startpage:endpage]
                                else:
                                    crossrefpages = ''

                                allauthors = ''
                                if '"given":"'in crossrefdata:

                                    numauthors = crossrefdata.count('"given":"')
                                    authorcount = str(numauthors)

                                    nextauthor = 0
                                    familyend = 1
                                    

                                    while nextauthor<numauthors and nextauthor<21:

                                        givenstart = crossrefdata.find('"given":"',familyend)+9

                                        givenend = crossrefdata.find('"',givenstart)

                                        given = crossrefdata[givenstart:givenend]
                                       

                                        familystart = crossrefdata.find('"family":"',givenend)+10
                                        familyend = crossrefdata.find('"',familystart)
                                        family = crossrefdata[familystart:familyend]
                                       
                                        authorname = family+', '+given

                                        if '"affiliation":[{"name":"' in crossrefdata[familyend:]:
                                            startaffil = crossrefdata.find('"affiliation":[{"name":"',familyend)+24
                                            endaffil = crossrefdata.find('"}]',startaffil)
                                            affil = crossrefdata[startaffil:endaffil]
                                            if '"},{"name":"' in affil:
                                                affil =  affil.replace('"},{"name":"',', ')
                                            
                                            affil = ': '+affil
                                        else:
                                            affil = ''
                                        authorname = authorname+affil
                                        
                                        if nextauthor == 0:
                                            allauthors = authorname
                                        else:
                                            allauthors = allauthors+'; '+authorname
                                        nextauthor += 1

                                elif 'author":[{"name":"' in crossrefdata:


                                    nextauthor = 0
                                    start = crossrefdata.find('author":[{"name":"')

                                    numauthors = crossrefdata.count('"name":',start)
                                    authorcount = str(numauthors)
                                    allauthors = ''

                                    while nextauthor<numauthors and nextauthor<21:

                                        namestart = crossrefdata.find('"name":',start)+8
                                        nameend = crossrefdata.find('"',namestart)
                                        authorname = crossrefdata[namestart:nameend]

                                        if '"affiliation":[{"name":"' in crossrefdata[nameend:]:
                                            startaffil = crossrefdata.find('"affiliation":[{"name":"',familyend)+24
                                            endaffil = crossrefdata.find('"}]',startaffil)
                                            affil = crossrefdata[startaffil:endaffil]
                                            if '"},{"name":"' in affil:
                                                affil =  affil.replace('"},{"name":"',', ')
                                            
                                            affil = ': '+affil
                                        else:
                                            affil = ''
                                        authorname = authorname+affil
                                        
                                        
                                        start = nameend
                                        if nextauthor == 0:
                                            allauthors = authorname
                                        else:
                                            allauthors = allauthors+'; '+authorname
                                        nextauthor += 1

                                elif 'author":[{"family":"'in crossrefdata:


                                    nextauthor = 0
                                    start = crossrefdata.find('author":[{"family":"')

                                    numauthors = crossrefdata.count('"family":"',start)
                                    authorcount = str(numauthors)
                                    allauthors = ''

                                    while nextauthor<numauthors and nextauthor<21:

                                        namestart = crossrefdata.find('"family":"',start)+10
                                        nameend = crossrefdata.find('"',namestart)
                                        authorname = crossrefdata[namestart:nameend]

                                        if '"affiliation":[{"name":"' in crossrefdata[nameend:]:
                                            startaffil = crossrefdata.find('"affiliation":[{"name":"',familyend)+24
                                            endaffil = crossrefdata.find('"}]',startaffil)
                                            affil = crossrefdata[startaffil:endaffil]
                                            if '"},{"name":"' in affil:
                                                affil =  affil.replace('"},{"name":"',', ')
                                            
                                            affil = ': '+affil
                                        else:
                                            affil = ''
                                        authorname = authorname+affil
                                        
                                        
                                        start = nameend
                                        if nextauthor == 0:
                                            allauthors = authorname
                                        else:
                                            allauthors = allauthors+'; '+authorname
                                        nextauthor += 1






                                else:
                                    #correspond_author = ''
                                    allauthors = ''

                                    authorcount = ''

                            
                            
                            if '\\u' in allauthors :
                                
                                for i,j in unicodereplace:
                                    
                                    allauthors2 = allauthors.replace(i,j)
                                    allauthors = allauthors2
                            allauthors = allauthors.replace('\\','')
                            
                           
                            if '"funder":[{' in crossrefdata:
                                fundercount = 0
                                funderstart = 0
                                crfunderlist = ''
                                startcrfunderdata = crossrefdata.find('"funder":[{')+11
                                endcrfunderdata = crossrefdata.find(']}],')
                                crfunderdata = crossrefdata[startcrfunderdata:endcrfunderdata]
                                numberofcrfunders = crfunderdata.count('"name":"')
                                while fundercount<numberofcrfunders:
                                    startcrfunder = crfunderdata.find('"name":"',funderstart)+8
                                    endcrfunder = crfunderdata.find('"',startcrfunder)
                                    crfunder = crfunderdata[startcrfunder:endcrfunder]
                                    
                                    funderstart = endcrfunder
                                    fundercount += 1
                                    if fundercount == 1:
                                        crfunderlist = crfunder
                                    else:
                                        crfunderlist = crfunderlist+'; '+crfunder

                            else:
                                crfunder = ''

                            if '\\u' in crfunderlist:
                                for i,j in unicodereplace:
                                    crfunderlist2 = crfunderlist.replace(i,j)
                                    crfunderlist = crfunderlist2

                            crfunderlist = crfunderlist.replace('\\','')
                            
                            if '"subject":["' in crossrefdata:
                                startcrossrefsubject = crossrefdata.find('"subject":["')+12
                                endcrossrefsubject = crossrefdata.find(']',startcrossrefsubject)
                                crossrefsubject= crossrefdata[startcrossrefsubject:endcrossrefsubject]
                                crossrefsubject = crossrefsubject.replace('\"','').replace(',','; ')
                            else:
                                crossrefsubject = ''

                            
                            
                            
                            #for issn in issnlist:
                           
                            if len(issnlist)>0:
                                if issnlist[0] in allapcissndict:
                                    
                                    publishercurrency = 'USD'
                                    publisherapc = allapcissndict.get(issnlist[0])

                                elif len(issnlist) == 2 and issnlist[1] in allapcissndict:
                                    
                                    publishercurrency = 'USD'
                                    publisherapc = allapcissndict.get(issnlist[1])    
                                

                                elif  journal in allapctitledict:
                                    
                                    publishercurrency = 'USD'
                                    publisherapc = allapctitledict.get(journal)

                                
                                elif 'American Physical Society (APS)' in publisher:
                                    if 'Physical Review Letters' in journal:
                                        publishercurrency = 'USD'
                                        publisherapc = '3500'
                                    elif 'Physical Review Applied' in journal:
                                        publishercurrency = 'USD'
                                        publisherapc = '2500'
                                    elif 'Physical Review X' in journal:
                                        publishercurrency = 'USD'
                                        publisherapc = '4000'
                                    elif 'Physical Review Physics Education Research' in journal:
                                        publishercurrency = 'USD'
                                        publisherapc = '2000'
                                    elif 'Physical Review' in journal:
                                        publishercurrency = 'USD'
                                        publisherapc = '2200'
                                    else:
                                        publishercurrency = ''
                                        publisherapc = ''

                                elif 'Emerald' in publisher:
                                    publishercurrency = 'USD'
                                    publisherapc = '3240'

                                elif 'American Society for Microbiology' in publisher:
                                    if 'Microbiology Resource Announcements' in journal:
                                        publishercurrency = 'USD'
                                        publisherapc = '1000'
                                    elif 'Journal of Microbiology & Biology Education' in journal or 'Microbiology and Molecular Biology Reviews' in journal:
                                        publishercurrency = 'USD'
                                        publisherapc = '0'
                                    
                                    else:
                                        publishercurrency = 'USD'
                                        publisherapc = '3500'

                                elif 'Royal Society of Chemistry' in publisher:
                                    publishercurrency = 'GBP'
                                    publisherapc = '1600'

                                elif 'American Chemical Society' in publisher:
                                    publishercurrency = 'USD'
                                    publisherapc = '4000'

                                elif 'CSIRO Publishing' in publisher:
                                    publishercurrency = 'USD'
                                    publisherapc = '2700'

                                elif 'Institute of Electrical and Electronics Engineers' in publisher:
                                    publishercurrency = 'USD'
                                    if journal == 'IEEE Access':
                                        publisherapc = '1750'
                                    else:
                                        publisherapc = '2045'


                            else:
                                publishercurrency = ''
                                publisherapc = ''

                            
                            if apccharged == 'No':
                                finalapc = '0'

                            elif len(publishercurrency)>2:

                                
                                finalcurrency = exchangeratedict['rates'][publishercurrency]

                                
                                finalapc = str(int(publisherapc)/finalcurrency)

                                if '.' in finalapc:
                                    finddot = finalapc.find('.')
                                    finalapc = finalapc[:finddot]

                            elif len(doajcurrency)>2:

                                
                                finalcurrency = exchangeratedict['rates'][doajcurrency]

                                finalapc = str(int(doajprice)/finalcurrency)

                                if '.' in finalapc:
                                    finddot = finalapc.find('.')
                                    finalapc = finalapc[:finddot]
                                
                            
                                
                            

                            else:
                                finalapc = ''

                                                
                            
                            
                            
                            
                            numberoflocalauthors = str(numberoflocalauthors)
                        
                            


                        
                            if numauthors>20:
                                morethan20authors = 'Yes'
                            else:
                                morethan20authors = 'No'
                                
                            
                            if len(localreprintauthor)>1:
                                reprintauthorislocal = 'Yes'
                            else:
                                reprintauthorislocal = 'No'

                            
                            
                            #Send the DOI to the altmetric API. 
                            print('Requesting Altmetric data')
                            findaltm = requests.get('https://api.altmetric.com/v1/doi/'+doi,timeout=(10,20))

                            #Read in the output from the API search to a page called altminfo.

                            altmpage = findaltm.content
                            altminfo = str(altmpage,encoding = 'utf-8')
                            for i,j in unicodereplace:
                                altminfo = altminfo.replace(i,j)
                            #altminfo = codecs.decode(altminfo,'unicode-escape')

                            print('Altmetric data returned')
                            if '"score":' in altminfo:

                                startscore = altminfo.find('"score":')+8
                                endscore = altminfo.find(',',startscore)
                                score = altminfo[startscore:endscore]
                            else:
                                score = '0'

                            if '"cited_by_msm_count":' in altminfo:
                                msmstart = altminfo.find('"cited_by_msm_count":')+21
                                msmend = altminfo.find(',',msmstart)
                                msmcount = altminfo[msmstart:msmend]
                            else:
                                msmcount = '0'


                            if '"cited_by_policies_count":' in altminfo:
                                policystart = altminfo.find('"cited_by_policies_count":')+26
                                policyend = altminfo.find(',',policystart)
                                policycount = altminfo[policystart:policyend]
                            else:
                                policycount = '0'

                            if '"cited_by_tweeters_count":' in altminfo:
                                tweetstart = altminfo.find('"cited_by_tweeters_count":')+26
                                tweetend = altminfo.find(',',tweetstart)
                                tweetcount = altminfo[tweetstart:tweetend]
                            else:
                                tweetcount = '0'

                            if '"details_url":"' in altminfo:
                                detailstart = altminfo.find('"details_url":"')+15
                                detailend = altminfo.find('"',detailstart)
                                detail = altminfo[detailstart:detailend]
                            else:
                                detail = ''

                            
                            

                            #create issn output
                            issnout = ''
                            for issn in issnlist:
                                issnout = issnout+issn+' '
                            
                            #Update the counts
                            if isoa == 'true':
                                isoacount += 1
                            
                           

                            if validdoi == 'y' and unpaywallfound == 'y':

                                

                               

                                

                                if '\\' in funders:
                                    for i,j in unicodereplace:
                                        funders = funders.replace(i,j)
                                

                                outlist.append(doi);outlist.append(evidence);outlist.append(licence);outlist.append(oastatus);outlist.append(title);outlist.append(allauthors);outlist.append(authorcount);outlist.append(morethan20authors);outlist.append(wosorscopusauthors);outlist.append(numberoflocalauthors);outlist.append(localauthorlist);outlist.append(reprintauthor);outlist.append(localreprintauthor);outlist.append(reprintauthorislocal);outlist.append(journal);outlist.append(year);outlist.append(publisher);outlist.append(isoa);outlist.append(genre);outlist.append(oajournal);outlist.append(version);outlist.append(host_type);outlist.append(greenavailable);outlist.append(repout);outlist.append(str(repositorycount));outlist.append(inlocalrepository);outlist.append(doaj);outlist.append(issnout);outlist.append(aamarchiving); outlist.append(aamembargo);outlist.append(publishedarchiving);outlist.append(publishedembargo);outlist.append(sherpalink);outlist.append(scopuscitations);outlist.append(citations);outlist.append(freetexturl);outlist.append(inwos);outlist.append(inscopus);outlist.append(apccharged);outlist.append(doajcurrency);outlist.append(doajprice);outlist.append(publishercurrency);outlist.append(publisherapc);outlist.append(finalapc);outlist.append(score);outlist.append(msmcount);outlist.append(policycount);outlist.append(tweetcount);outlist.append(detail);outlist.append(funders);outlist.append(crfunderlist);outlist.append(wossubject);outlist.append(crossrefsubject);outlist.append(crossrefpages)
                                #Write the data to the .CSV file
                                
                                

                                writer.writerow(outlist)

                               
                                
                                print(str(didnotexecutelist))
                                
                            else:
                                row = [doi,'DOI not found in unpaywall']
                            

                            

                            
                            print('Saving')


                            

                            #Pause to avoid overloading the APIs
                            time.sleep(2)
                            print(str(datetime.datetime.now())[11:19])

                            print()
                            

                            #Update the count
                            
                            processedcount += 1
                            
                            
                            
                            #Sent progress information to the screen

                            print(str(linecount)+' lines read')
                            
                            print(str(linecount)+'/'+str(recordcount)+' lines processed ('+str(int((linecount/recordcount)*100))+'%)')
                            errors = notfoundcount+outsiderangecount
                            
                            validlines = linecount-errors
                            

                            print(str(validlines)+' valid lines')
                            
                            
                            if processedcount-errors>0:
                                oaperc =  str(int((isoacount/validlines)*100))
                                oaperc = '('+oaperc+'%)'
                                print(str(isoacount)+' OA documents found '+oaperc)

                            print(str(errors)+' errors')
                            print(str(notfoundcount)+' DOIs not found')
                            
                            
                            print(str(outsiderangecount)+ ' DOIs outside year range')
                            print(str(unexecutedcount)+' lines did not execute')
                            
                            now = datetime.datetime.now()
                            timetaken = now-nowstart2
                            timetakenstr = str(timetaken)
                            finddot = timetakenstr.find('.')
                            
                            estimatedtime = (timetaken/processedcount)*(recordcount-processedcount)
                            estimatedcompletion = str(now+estimatedtime)
                            estimatedtimestr = str(estimatedtime)
                            finddot2 = estimatedtimestr.find('.')
                            
                            startcomptime = estimatedcompletion.find(' ')+1
                            endcomptime = estimatedcompletion.find('.')
                            print(str(estimatedcompletion[startcomptime:endcomptime]))

                                


                            print()


                            #End of processing for the row. Program continues until the last row is completed.
                            


                        
                            if unpaywallfound == 'n':
                                writer.writerow(outlist)
                                
                                print('Saving')
                                print()
                            
                                
                                
                                    
                            
                    else:
                        print('Year outside range')
                    
                        recorderror.write('"'+doi+'","Year outside range - '+str(year)+'"\n')
                        
                        
                        outsiderangecount += 1
                        processedcount += 1
                        print()
                else:
                    if validdoi == 'y':
                        
                    
                        recorderror.write('"'+doi+'","DOI not in crossref"\n')
                    
                    print('DOI not in crossref')
                    print()
                    
                    notfoundcount += 1
                done = 'y'
            except:
                time.sleep(10)
                retrycount += 1
                print(retrycount)
                
                print('Line did not execute')
                
                if retrycount == 8:
                    unexecutedcount += 1
                    recorderror.write('"'+doi+'","Line did not execute"\n')
                    didnotexecutelist.append(doi)
                continue
#After completion of the final row the repository data is aggregated.
#Create an output csv file

ofile = str(inf+'_'+now1+'_repositories.csv')


rel_path = newdir+"/"+ofile

abs_file_path =  os.path.join(script_dir, rel_path)

of2 = abs_file_path

of2 = abs_file_path


#fout2 = open(of2, 'w')


#Convert the repository data  list to a string
pmhliststring = str(pmhlist)

#Sort the repository list
repositorylist.sort()


#Create an output list for the aggregated repository data
replistout = []
#Create headings
headings = ['Repository','Items','Published Version','Accepted Version','Submitted Version','Null']
with open(of2, 'w', newline = '',encoding = 'utf-8') as outputfile:
    writer =  csv.writer(outputfile)
    writer.writerow(headings)


#Sent the headings to the output file



#Aggregate the data for each repository in the repository list
for repository in repositorylist:
    #Count the number of hits for the repository
    repcount = pmhliststring.count(repository)
      

    #Create a search to find all instances of  publishedVersion for that repository
    pvfind = repository+'', 'publishedVersion'
    #This gets output as a tuple so needs to be converted to a string without brackets
    pvfind = str(pvfind).replace('(','')
    pvfind = str(pvfind).replace(')','')
    publishedversioncount = pmhliststring.count(pvfind)

    avfind = repository+'', 'acceptedVersion'
    avfind = str(avfind).replace('(','')
    avfind = str(avfind).replace(')','')
    acceptedversioncount = pmhliststring.count(avfind)

    svfind = repository+'', 'submittedVersion'
    svfind = str(svfind).replace('(','')
    svfind = str(svfind).replace(')','')
    submittedversioncount = pmhliststring.count(svfind)

    nvfind = repository+'', 'null'
    nvfind = str(nvfind).replace('(','')
    nvfind = str(nvfind).replace(')','')
    nullversioncount = pmhliststring.count(nvfind)

    #Send data to the output list
    replistout.append(repository)
    replistout.append(str(repcount))
    replistout.append(str(publishedversioncount))
    replistout.append(str(acceptedversioncount))
    replistout.append(str(submittedversioncount))
    replistout.append(str(nullversioncount))
    

    #Write the list to the output file
    #fout2.write('"')
    #fout2.write('","'.join(replistout))
    #fout2.write('"\n')
    with open(of2, 'a', newline = '',encoding = 'utf-8') as outputfile:
        writer =  csv.writer(outputfile)
        writer.writerow(replistout)

    #Clear the repository list ready for the next loop
    replistout = []

statuslist = ['closed','gold','diamond','bronze','green','hybrid']

headinglist = ['Funder','closed','gold','diamond','bronze','green','hybrid','Total','% Open','Closed/AAM embargoed','Closed/AAM immediate','Potential % open']

print('len(funderlist) = '+str(len(funderlist)))

if len(funderlist)>0:

    funderlist.sort()

    
    fundercount = []

    ofile = str(inf+'_'+now1+'_funders.csv')

    rel_path = newdir+"/"+ofile
    abs_file_path =  os.path.join(script_dir, rel_path)

    

    of3 = abs_file_path
    #print(funderlist)
    

    
    

    
    
    
    
    
    with open(of3, 'w', newline = '',encoding = 'utf-8') as outputfile:
        writer =  csv.writer(outputfile)
        writer.writerow(headinglist)
        outputfile.close()

        funderdata = str(funderdata)

        

        for i,j in unicodereplace:

            funderdata = funderdata.replace(i,j)
            
        
        
        

        for funder in funderlist:
            funderlistout = []
            totalstatus = 0
            
            

            funderlistout.append(funder)

            for status in statuslist:
                
                statuscount = funderdata.count('\''+funder+'\', \''+status)
                #print('statuscount for '+status+' = '+str(statuscount))
                totalstatus = totalstatus+statuscount
                if totalstatus == 0:
                    statuscount = funderdata.count('\"'+funder+'\", \''+status)
                    totalstatus = totalstatus+statuscount


                funderlistout.append(str(statuscount))
                
                
                
            

            funderlistout.append(str(totalstatus))
            

            closedcount = funderdata.count('\''+funder+'\', \'closed')
            #print('totalstatus = '+str(totalstatus))
            #print('closedcount = '+str(closedcount))
            if totalstatus>0:
                opencount = totalstatus-closedcount
                #if totalstatus<0:
                percopen = (opencount/totalstatus)*100
                percopen = str(percopen)
                finddot = percopen.find('.')
                percopen = percopen[:finddot]
            else:
                percopen = '0'
            

            

            funderlistout.append(percopen)

            #potentialaamembargocount = statuscount = funderdata.count('\''+funder+'\', \'closed''\', \'e')
            #potentialaamcancount = statuscount = funderdata.count('\''+funder+'\', \'closed''\', \'y')

            potentialaamembargocount = funderdata.count('\''+funder+'\', \'closed''\', \'e')
            potentialaamcancount = funderdata.count('\''+funder+'\', \'closed''\', \'y')

            potentialaamopen = opencount+potentialaamembargocount+potentialaamcancount

            funderlistout.append(potentialaamembargocount);funderlistout.append(potentialaamcancount)

            
            if totalstatus>0:
                perpotentialaamopen = str((potentialaamopen/totalstatus)*100)
                finddot = perpotentialaamopen.find('.')
                perpotentialaamopen = perpotentialaamopen[:finddot]
            else:
                
                perpotentialaamopen = '0'

            funderlistout.append(perpotentialaamopen)

            
            
           
            
            try:
                with open(of3, 'a', newline = '',encoding = 'utf-8') as outputfile2:
                    writer =  csv.writer(outputfile2)
                    writer.writerow(funderlistout)
            except:
                print('Row did not print!')
                print(funderlistout)
                continue


   

if wosused == 'Yes':
    headinglist2 = ['WoS Subject','closed','gold','diamond','bronze','green','hybrid','Total','% Open','Closed/AAM embargoed','Closed/AAM immediate','Potential % open']

    ofile = str(inf+'_'+now1+'_subjects.csv')

    subjectlist.sort()

    rel_path = newdir+"/"+ofile
    abs_file_path =  os.path.join(script_dir, rel_path)

    of4 = abs_file_path

    with open(of4, 'w', newline = '',encoding = 'utf-8') as outputfile:
        writer =  csv.writer(outputfile)
        writer.writerow(headinglist2)

    



    subjectdata = str(subjectdata)
    
    

    
    for subject in subjectlist:
        
    
        subjectlistout = []
        totalstatus = 0

        subjectlistout.append(subject)
        #closedcount = 0
        for status in statuslist:
            

            statuscount = subjectdata.count('\''+subject+'\', \''+status)
            
            totalstatus = totalstatus+statuscount
            if totalstatus == 0:
                statuscount = subjectdata.count('\"'+subject+'\", \''+status)
                totalstatus = totalstatus+statuscount


            subjectlistout.append(str(statuscount))
            if status == 'closed':
                closedcount = statuscount
            
        
        subjectlistout.append(str(totalstatus))
        closedcount = subjectdata.count('\''+subject+'\', \'closed')
        
        if totalstatus>0:
            opencount = totalstatus-closedcount
            percopen = (opencount/totalstatus)*100
            percopen = str(percopen)
            finddot = percopen.find('.')
            percopen = percopen[:finddot]
            

            
            subjectlistout.append(percopen)

                        
            potentialaamembargocount = statuscount = subjectdata.count('\''+subject+'\', \'closed''\', \'e')
            
            potentialaamcancount = statuscount = subjectdata.count('\''+subject+'\', \'closed''\', \'y')
            

            potentialaamopen = opencount+potentialaamembargocount+potentialaamcancount
            
            perpotentialaamopen = str((potentialaamopen/totalstatus)*100)
            finddot = perpotentialaamopen.find('.')
            perpotentialaamopen = perpotentialaamopen[:finddot]
            

            subjectlistout.append(potentialaamembargocount);subjectlistout.append(potentialaamcancount);subjectlistout.append(perpotentialaamopen)
            
        else:
            percopen = '0'
            perpotentialaamopen = '0'


        



        with open(of4, 'a', newline = '',encoding = 'utf-8') as outputfile:
            writer =  csv.writer(outputfile)
            writer.writerow(subjectlistout)
    


if wosused == 'Yes' or scopusused == 'Yes':
    headinglist2 = ['Department','closed','gold','diamond','bronze','green','hybrid','Total','% Open','Closed/AAM embargoed','Closed/AAM immediate','Potential % open']
    headinglist3 = ['Department','Total','closed','gold','diamond','bronze','green','hybrid','Journal articles','Open','% Open','Closed/AAM embargoed','Closed/AAM immediate','Potential % open']

    ofile = str(inf+'_'+now1+'_departments.csv')

    departmentlist.sort()
    print(str(departmentlist))

    rel_path = newdir+"/"+ofile
    abs_file_path =  os.path.join(script_dir, rel_path)

    of5 = abs_file_path



    with open(of5, 'w', newline = '',encoding = 'utf-8') as outputfile:
        writer =  csv.writer(outputfile)
        writer.writerow(headinglist3)


    departmentdata = str(departmentdata)
    
    
    


    #for department in departmentlist:
    for i in range(0,len(departmentlist)):
        department = departmentlist[i]
        
        departmenttotal = departmentdata.count('\''+department+'\'')
        if departmenttotal == 0:
            departmenttotal = departmentdata.count('\"'+department+'\"')

        
        
        departmentlistout = []
        totalstatus = 0

        departmentlistout.append(department);departmentlistout.append(departmenttotal)
        
        closedcount = 0
        
        for status in statuslist:
            
            

            #statuscount = departmentdata.count('\''+department+'\', \''+status)
            
            statuscount = departmentdata.count('\''+department+'\', \'journal-article\', \''+status) + departmentdata.count('\''+department+'\', \'not-journal-article\', \''+status)

            totalstatus = totalstatus+statuscount
            if totalstatus == 0:
                #statuscount = departmentdata.count('\"'+department+'\", \''+status)
                statuscount = departmentdata.count('\"'+department+'\", \'journal-article\', \''+status) + departmentdata.count('\"'+department+'\", \'not-journal-article\', \''+status)
                totalstatus = totalstatus+statuscount


            departmentlistout.append(str(statuscount))
            if status == 'closed':
                closedcount = statuscount
            
        journalarticlecount = departmentdata.count('\''+department+'\', \'journal-article')
        
        journalarticleclosedcount = departmentdata.count('\''+department+'\', \'journal-article\', \'closed')
        
        journalarticleopencount = journalarticlecount - journalarticleclosedcount
        departmentlistout.append(str(journalarticlecount))
        departmentlistout.append(str(journalarticleopencount))

        

        
        #closedcount = departmentdata.count('\''+department+'\', \'closed')
        #if totalstatus>0 and len(department)>0:
        if departmenttotal>0 and len(department)>0:
            #opencount = totalstatus-closedcount
            #opencount = departmenttotal-closedcount
            #percopen = (opencount/totalstatus)*100
            if journalarticlecount>0:
                percopen = (journalarticleopencount/journalarticlecount)*100
                percopen = str(percopen)
                finddot = percopen.find('.')
                percopen = percopen[:finddot]+'%'
            else:
                percopen=''
            
            departmentlistout.append(percopen)
            #potentialaamembargocount = statuscount = departmentdata.count('\''+department+'\', \'closed''\', \'e')

            potentialaamembargocount = departmentdata.count('\''+department+'\', \'journal-article\', \'closed''\', \'e')
            
            
            potentialaamcancount  = departmentdata.count('\''+department+'\', \'journal-article\', \'closed''\', \'y')

            potentialaamopen = journalarticleopencount+potentialaamembargocount+potentialaamcancount

            perpotentialaamopen = str((potentialaamopen/totalstatus)*100)
            finddot = perpotentialaamopen.find('.')
            perpotentialaamopen = perpotentialaamopen[:finddot]+'%'

            departmentlistout.append(potentialaamembargocount);departmentlistout.append(potentialaamcancount);departmentlistout.append(perpotentialaamopen)


            
        else:
            
            percopen = '0'
            perpotentialaamopen = '0'
        
        try:
            
            with open(of5, 'a', newline = '',encoding = 'utf-8') as outputfile:
                writer =  csv.writer(outputfile)
                writer.writerow(departmentlistout)

        except:
            print('Row did not print!')
            
            continue
    


  
  

ofile = str(inf+'_'+now1+'_summary.txt')



rel_path = newdir+"/"+ofile
abs_file_path =  os.path.join(script_dir, rel_path)

of6 = abs_file_path



fout6 = open(of6, 'w')
fout6.write(str(linecount)+' lines read\n')
            
fout6.write(str(processedcount)+'/'+str(recordcount)+' lines processed ('+str(int((processedcount/recordcount)*100))+'%)\n')



fout6.write(str(validlines)+' valid lines\n')


if processedcount-errors>0:
    oaperc =  str(int((isoacount/validlines)*100))
    oaperc = '('+oaperc+'%)'
    fout6.write(str(isoacount)+' OA documents found '+oaperc+'\n')

fout6.write(str(errors)+' errors\n')
fout6.write(str(notfoundcount)+' DOIs not found\n')
fout6.write(str(outsiderangecount)+ ' DOIs outside year range\n')
fout6.write(str(unexecutedcount)+ ' lines not executed\n')
fout6.write('\n')
fout6.write('Input file\t')
fout6.write(infilestring+'\n')
fout6.write('Web of Science file:\t')
if wosused == 'Yes':
    fout6.write(wosfilestring+'\n')
else:
    fout6.write('None\n')
fout6.write('Scopus file:\t')
if scopusused  == 'Yes':
    fout6.write(scopusfilestring+'\n')
else:
    fout6.write('None\n')
fout6.write('Repository address:\t')
if len(repstring)>0:
    fout6.write(repstring+'\n')
else:
    fout6.write('None\n')
if wosused == 'Yes':
    fout6.write('Web of Science institutional address:\t')
    fout6.write(instita+'\n')
    if len(institb)>0:
        fout6.write('Web of Science alternative institutional address:\t')
        fout6.write(institb+'\n')
if scopusused == 'Yes':
    fout6.write('Scopus institutional address\t')
    fout6.write(scopusinstnamea+'\n')
    if len(scopusinstnameb)>0:
        fout6.write('Scopus alternative institutional address\t')
        fout6.write(scopusinstnameb+'\n')
fout6.write('Year span:\t')
fout6.write(str(startyear)+'-'+str(endyear))

fout6.close()
recorderror.close()

print('Finished!')
i = input('Press any key to exit')