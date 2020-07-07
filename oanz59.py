#!/usr/bin/env python
# -*- coding: utf-8 -*
#Open Access API Project
import requests
import re
import datetime
import time
import csv
import os
import codecs
import json

#Values are read in from the file keys.txt which is held in the same folder as the program
#The first line is a header, the second is a valid key for Sherpa/Romeo, the third is a valid email address used as part of the unpaywall API search
#https://www.sherpa.ac.uk/romeo/apiregistry.php

#https://unpaywall.org/products/api



try:
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    rel_path = "input_files/keys.txt"
    abs_file_path4 = os.path.join(script_dir, rel_path)
    print(abs_file_path4)
    file=abs_file_path4 
    keyfile=open(file)
    keyfile.readline()
    sherpakey = keyfile.readline()
 
    sherpakey=sherpakey[:-1]
    

    emailaddress = keyfile.readline()
    
except:
    print('File "keys.txt" not found in folder input_files')
    quit()

#Create two folders within the same folder that the program file is stored – Input and Output
#Verify input file and quit if not found
#The input file will be a single column CSV file headed 'DOI' listing all DOIs to be processed. 
#It is stored in the Input folder



inf=input('Enter the name of the input file: ')
infilestring=str(inf)
print(infilestring)
if '.csv' not in infilestring.lower():
    infilestring=infilestring+'.csv'

#Locate the input file and quit if it is not found

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = "input_data/"+infilestring
abs_file_path = os.path.join(script_dir, rel_path)

doi_list=abs_file_path
print(doi_list)

try:
    filetest=open(doi_list)

except:
    print("File not found")
    quit()

#A csv file from Web of Science is now imported to provide author affiliation and funder detail. This file will have been created by 
# searching WoS for the DOIs in the input file and then exporting them as full records in Tab-delimited UTF-8 format. 
# This file is placed in the Input folder
#Do an advanced search in WoS using the format 
# DO=10.1080/21680566.2017.1377646 OR DO=10.1080/13573322.2017.1391085
wostry=0
wosfound='n'
while wostry<3 and wosfound=='n':

    wosname=input('Enter the name of the WoS file or press Enter to skip: ')
    
    if len(wosname)>0:
        
        wosused='Yes'
        wosfilestring=str(wosname)
        if '.csv' not in wosfilestring.lower():
            wosfilestring=wosfilestring+'.csv'

        script_path = os.path.abspath(__file__)
        script_dir = os.path.split(script_path)[0]
        rel_path = "input_data/"+wosfilestring
        abs_file_path2 = os.path.join(script_dir, rel_path)

        wosfile=abs_file_path2


        try:
            filetest=open(wosfile)
            wosfound='y'

        except:
            print("File not found") 
            
            wostry+=1
            if wostry<3:
                print('Try again')
                
            else:
                print('Too many tries')
                quit()
    else:
        wosused='No'
        wosfound='y'

#A Scopus file based on a search for the DOIs in the input file is now imported. 
#It is exported as a csv file and must include the Affiliation field. Scopus csv files
#automatically export in comma-delimited format
#Do and advanced search in Scopus using the format 
# DOI(10.1080/21680566.2017.1377646 )  OR  DOI(10.1080/13573322.2017.1391085 )
#Include all funding details except Funding text which will use multiple columns and distort the output

scotry=0
scofound='n'
while scotry<3 and scofound=='n':
    scopusfilename=input('Enter the name of the Scopus file or press Enter to skip: ')
    
    if len(scopusfilename)>0:
        scopusused = 'Yes'
        scopusfilestring=str(scopusfilename)
        if '.csv' not in scopusfilestring.lower():
            scopusfilestring=str(scopusfilename)+'.csv'




        script_path = os.path.abspath(__file__)
        script_dir = os.path.split(script_path)[0]
        rel_path = "input_data/"+scopusfilestring
        abs_file_path2 = os.path.join(script_dir, rel_path)

        scofile=abs_file_path2
        
        
        try:
            filetest=open(scofile)
            scofound='y'

        except:
            print("File not found")
            scotry+=1
            if scotry<3:
             print('Try again')
            else:  
                print('Too many tries') 
                quit()
    else:
        scopusused='No'
        scofound='y'



repstring=input('Repository address, eg.g researchcommons.waikato.ac.nz: ')
#repstring='researchcommons.waikato.ac.nz'
#repstring='researcharchive.lincoln.ac.nz'
#repstring='researchspace.auckland.ac.nz'
#repstring='ourarchive.otago.ac.nz'
#repstring='mro.massey.ac.nz'


if wosused=='Yes':

    instita=input('Enter the name of the institution in Web of Science format (e.g. Univ Auckland): ')
    institb=input('Enter alternative name: ')
    #instita='Massey Univ'
    #institb=''
else:
    instita=''
    institb=''

if scopusused=='Yes':
    scopusinstnamea=input('Enter the name of the institution in Scopus format (e.g. University of Auckland): ')
    scopusinstnameb=input('Enter the alternative name of the institution in Scopus format: ')
    #scopusinstnamea='Massey University'
    #scopusinstnameb=''
else:
    scopusinstnamea=''
    scopusinstnameb=''

yearcorrect='n'
yearcount=0
while yearcorrect=='n' and yearcount<3:
   
    yearspan=input('Enter years to span in the format 2016-2018: ')
    
    if len(yearspan)!=9 or yearspan[4]!='-':
        print('Invalid entry')
        yearcount+=1
        if yearcount==3:
            print('Too many tries')
            quit()
        else:
            print('Try again')
    else:
        yearcorrect='y'
startyear=int(yearspan[0:4])



endyear=int(yearspan[5:9])

#Import the Sherpa/Romeo list
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = "input_files/sherpalist.csv"
abs_file_path4 = os.path.join(script_dir, rel_path)
sherpafile=abs_file_path4 

#Create output file with date and time included in filename
nowstart=datetime.datetime.now()
now1=str(nowstart)
now1=now1.replace(':','-')
now1=now1.replace(' ','-')
now1=now1[:16]


ofile=str(inf+'_'+now1+'.csv')

#Create path to output file in output folder

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
newdir="output/"+inf+'_'+now1
os.makedirs(newdir)

rel_path=newdir+"/"+ofile




abs_file_path3 = os.path.join(script_dir, rel_path)
#abs_file_path3 = os.path.join(script_dir, newdir)

of1=abs_file_path3


print(of1)


with open(of1, 'w', newline='',encoding='utf-8-sig') as outputfile:

#Headings for output file

    headings=['DOI','Evidence','Licence','OA Status','Title','Authors','Author count','Author count>20','WoS/Scopus Authors','Local author count from WoS/Scopus','Local authors','Corresponding author','Local reprint authors','Local reprint author address','Corresponding author is local','Journal','Year','Publisher','Is OA','Genre','OA Journal','Version','Host of best version','Green version available','Repositories','Number of repositories','In local repository','In DOAJ','ISSNs','Archive accepted manuscript','Archive published version','Sherpa/Romeo colour','Sherpa/Romeo Licence','Crossref citations','Free text url','In WoS','APC charged in DOAJ','DOAJ Currency','DOAJ APC','Publisher Currency','Publisher APC','USD APC','Altmetric','Media stories','Policy documents','Tweets','Altmetric link','Funders','Crossref funders','Subjects']
    writer = csv.writer(outputfile)
    writer.writerow(headings)
    

    efile=str(inf+'_'+now1+'_errors.csv')

    rel_path=newdir+"/"+efile
    abs_file_path = os.path.join(script_dir, rel_path)

    ef=abs_file_path

    foute=open(ef, 'w')

    foute.write('"DOI","Error"')
    foute.write('\n')

    #Set up the lists and counts


    #pmhlist records each instance of an item in a repository
    pmhlist=[]
    funderdata=[]
    funderlist=[]
    subjectdata=[]
    subjectlist=[]
    departmentlist=[]
    departmentdata=[]
    #repositorylist is a complete list of repositories that is output at the end of the program to aggregate the data from pmhlist
    repositorylist=[]
    didnotexecutelist=[]


    count=0
    linecount=0
    errors=0
    recordcount=0
    notfound=0
    notinsherpacount=0

    #truecount counts the rows for which OA status is true
    truecount=0
    outsiderangecount=0
    unexecuted=0

    print()




    wosdict=dict()

    doajdict=dict()

    allapcissndict=dict()
    allapctitledict=dict()
    scopusdict=dict()
    sherpadict=dict()
    crossrefissndict=dict()

   
    unicodefilestring='unicodelist.csv'

    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    rel_path = "input_files/"+unicodefilestring
    abs_file_path2 = os.path.join(script_dir, rel_path)

    unicodefile=abs_file_path2

    tfile=open(unicodefile,encoding='utf-8')
    records=csv.reader(tfile)
    unicodereplace=[]
    for line in records:
        outlist=[]
        coded=line[0]
        uncoded=line[1]
        
        outlist.append(coded); outlist.append(uncoded)
        output=tuple(outlist)
        unicodereplace.append(output)
       

    findyearlist=('"start":{"date-parts":[[','"published-print":{"date-parts":[[','"published-online":{"date-parts":[[','"created":{"date-parts":[[')

   
    punctreplace=[('’','\''),('‘','\''),('“','\"'),('”','\"')]

    #Create Sherpa/Romeo dictionary. This is used to avoid frequent use of the Sherpa API and is based on past capture of data. 

    sherpadata=csv.DictReader(open(sherpafile,encoding='utf-8-sig'))
    for line in sherpadata:
        sherpaissn=line['ISSN']
        sherpaacm=line['Archive accepted manuscript']
        sherpaapv=line['Archive published version']
        sherpacol=line['Sherpa/Romeo colour']
        sherpalic=line['Sherpa/Romeo Licence']
        sherpajournal=line['Journal']
        sherpaupdate=line['Updated']
        
        sherpadict[sherpaissn]=(sherpaacm,sherpaapv,sherpacol,sherpalic,sherpajournal,sherpaupdate)
   
    if wosused == 'Yes':

        wosdata=csv.DictReader(open(wosfile))
        for line in wosdata:
            
            wosdoi=line['DI']
            wosauthors=line['C1']
            wosauthors=wosauthors.replace('\'','')
            wosreprintauthor=line['RP']
            wosreprint=wosreprintauthor.replace('\'','')
            wosfund=line['FU']

            
            
            for i,j in unicodereplace:
                wosfund=wosfund.replace(i,j)

            wossubject=line['SC']
            wostitle=line['TI']

            wosreprintauthor=line['RP']
            wosauthors==line['C1']
            
            
        
            instit=instita
            if len(institb)>1 and institb in wosauthors:
                instit=institb
            
            allinstitcount=wosauthors.count('[')
            localinstitcount=wosauthors.count(instit)
            
            institposition=wosauthors.find(instit)

            institplace=wosauthors[:institposition].count('[')
        
            woslocalauthorlist=[]
            start=0
            #foundinstit=0
            localiteration=0
            totalcount=0
            authorininstit='y'
            if institplace>1:
                bracketcount=1
            else:
                bracketcount=1

            while bracketcount<institplace:

                start=wosauthors.find(']',start+1)


                bracketcount+=1



            if localiteration<localinstitcount:
                #foundinstit=0
                rightbracketposition=0


                while rightbracketposition<institposition  and authorininstit=='y':

                    finalauth='n'
                    leftbracketposition=wosauthors.find('[',start)
                    rightbracketposition=wosauthors.find(']',leftbracketposition)
                    start=rightbracketposition
                    woslocalauthors=wosauthors[leftbracketposition:rightbracketposition]
                    nextinstit=wosauthors[rightbracketposition+2:]

                    if (']') in nextinstit:
                        nextinstitend=nextinstit.find('[')
                        nextinstit=nextinstit[:nextinstitend]

                    if instit in nextinstit:
                        authorininstit='y'
                    else:
                        authorininstit='n'

                    if leftbracketposition==-1:
                        woslocalauthors=wosauthors[leftbracketposition:]

                    woslocalauthorcount=woslocalauthors.count(';')+1
                    authoriteration=0
                    wosauthorstart=1
                    while authoriteration<woslocalauthorcount and authorininstit=='y':


                        while finalauth=='n':

                            if ';' in woslocalauthors:
                                
                                endauthor=woslocalauthors.find(';',wosauthorstart)
                                woslocalauthor=woslocalauthors[wosauthorstart:endauthor]
                                woslocalauthors=woslocalauthors[endauthor+1:]
                                authoriteration+=1

                            else:
                                woslocalauthor=woslocalauthors[1:len(woslocalauthors)]
                                authoriteration+=1
                                finalauth='y'


                            if woslocalauthor not in woslocalauthorlist:
                                woslocalauthorlist.append(woslocalauthor)


                            institposition=wosauthors.find(instit,rightbracketposition)

                    localiteration+=1

            
            woslocalauthorlist=str(woslocalauthorlist)
            woslocalauthorlist=woslocalauthorlist.replace('\', \'','; ')
            woslocalauthorlist=woslocalauthorlist.replace(']','')
            woslocalauthorlist=woslocalauthorlist.replace('[','')
            woslocalauthorlist=woslocalauthorlist.rstrip()
            lengthaulist=len(woslocalauthorlist)

            if ';' in woslocalauthorlist:
                if woslocalauthorlist[lengthaulist-3]==';':

                    woslocalauthorlist=woslocalauthorlist[:lengthaulist-3]


                

            if len(woslocalauthorlist)>2:
                numberofwoslocalauthors=woslocalauthorlist.count(';')+1
            else:
                numberofwoslocalauthors=0


            woslocalauthorlist=woslocalauthorlist.replace(', \'\'','')
            woslocalauthorlist=woslocalauthorlist.replace('\'','')


        
            woslocalreprintauthor=''
            woslocalreprintauthoraddress=''
            instit=instita
            if len(institb)>1 and institb in wosreprintauthor:
                instit=institb
            if instit in wosreprintauthor:
                
                endauthor=0
                counter=0
                start=0
                startinstit=wosreprintauthor.find(instit)
                wosreprintauthorfound='n'
                semicolon=wosreprintauthor.find(';')
                nextsemicolon=0
                numberofreprintwosauthors=wosreprintauthor.count(';')+1

                if startinstit<semicolon:
                    startauthor=0
                    endauthor=wosreprintauthor.find('(')-1
                    woslocalreprintauthor=wosreprintauthor[startauthor:endauthor]
                    startwoslocalreprintauthoraddress=wosreprintauthor.find(instit)
                    woslocalreprintauthoraddress=wosreprintauthor[startwoslocalreprintauthoraddress:]
                    if ';' in woslocalreprintauthoraddress:
                        findsemi=woslocalreprintauthoraddress.find(';')
                        woslocalreprintauthoraddress=woslocalreprintauthoraddress[:findsemi]
                    
                   
                    wosdict[wosdoi]=(wosauthors,woslocalauthorlist,numberofwoslocalauthors,wosreprintauthor,woslocalreprintauthor,woslocalreprintauthoraddress,wostitle,wossubject,wosfund)  

                else:
                    while wosreprintauthorfound=='n' and counter<=numberofreprintwosauthors :

                        nextsemicolon=wosreprintauthor.find(';',start)

                        if nextsemicolon!=-1:

                            address=wosreprintauthor[semicolon+1:nextsemicolon+1]

                            start=nextsemicolon+2

                        else:

                            address=wosreprintauthor[start:]

                        if instit in address:
                            wosreprintauthorfound='y'
                            endauthor=address.find('(')-1
                            woslocalreprintauthor=address[:endauthor]
                            startwoslocalreprintauthoraddress=wosreprintauthor.find(instit)
                            woslocalreprintauthoraddress=wosreprintauthor[startwoslocalreprintauthoraddress:]
                            if ';' in woslocalreprintauthoraddress:
                                findsemi=woslocalreprintauthoraddress.find(';')
                                woslocalreprintauthoraddress=woslocalreprintauthoraddress[:findsemi]
                            
                            

               
                wosdict[wosdoi]=(wosauthors,woslocalauthorlist,numberofwoslocalauthors,wosreprintauthor,woslocalreprintauthor,woslocalreprintauthoraddress,wostitle,wossubject,wosfund)
             
            wosdict[wosdoi]=(wosauthors,woslocalauthorlist,numberofwoslocalauthors,wosreprintauthor,woslocalreprintauthor,woslocalreprintauthoraddress,wostitle,wossubject,wosfund)
          
        wosdict[wosdoi]=(wosauthors,woslocalauthorlist,numberofwoslocalauthors,wosreprintauthor,woslocalreprintauthor,woslocalreprintauthoraddress,wostitle,wossubject,wosfund)
        


    if scopusused=='Yes':
        

        scodata=csv.DictReader(open(scofile,mode="r", encoding="utf-8-sig"))
        
        for line in scodata:
            
            
            scopusdoi=line['DOI']
            scopusauthors=line['Authors']
            scopusfullauthors=line['Authors with affiliations']
            scopusreprintauthor=line['Correspondence Address']
            scopusfunders=line['Funding Details']
            scopusfunders=scopusfunders.replace('\n',';')
            scopusfunders=scopusfunders.replace(';;','; ')
           
            for i,j in unicodereplace:
                scopusfunders=scopusfunders.replace(i,j)
           
            

            

            for i,j in punctreplace:
                scopusauthors=scopusauthors.replace(i,j)
                scopusfullauthors=scopusfullauthors.replace(i,j)
                scopusreprintauthor=scopusreprintauthor.replace(i,j)
            

            
            
            
            
            #Select first 20 Scopus authors only
            start=0
            if scopusauthors.count(',')>20:
                authorcount=0

                while authorcount<20:
                    end=scopusauthors.find(',',start)
                    authorcount+=1
                    start=end+1
                scopusauthors=scopusauthors[:end]

            #Detect local reprint author
            scopuslocalreprintauthor=''
            scopuslocalreprintauthoraddress=''
            if scopusinstnamea in scopusreprintauthor:
                
                semicolon=scopusreprintauthor.find(';')
                
                scopuslocalreprintauthor=scopusreprintauthor[:semicolon]
                endaddress=scopusreprintauthor.find(';',semicolon+1)
                scopuslocalreprintauthoraddress=scopusreprintauthor[semicolon+2:endaddress]
                
                
            elif len(scopusinstnameb)>1 and scopusinstnameb in scopusreprintauthor:
                semicolon=scopusreprintauthor.find(';')
                scopuslocalreprintauthor=scopusreprintauthor[:semicolon+1]
                endaddress=scopusreprintauthor.find(';',semicolon)
                scopuslocalreprintauthoraddress=scopusreprintauthor[semicolon+2:endaddress]
            else:
                scopuslocalreprintauthor=''
                scopuslocalreprintauthoraddress=''

            
            

            
            

            #Extract local authors
            scopuslocalauthors=''
            localreprintauthor=''
            start=0
            authorcount=0
            scopuslocalauthorcount=0
            numberofscopusauthors=scopusfullauthors.count(';')+1
        
            while authorcount<numberofscopusauthors:
                endauthor=scopusfullauthors.find(';',start)
                thisauthor=scopusfullauthors[start:endauthor]
                if scopusinstnamea in thisauthor or (scopusinstnameb in thisauthor and len(scopusinstnameb)>1):
                    firstcomma=thisauthor.find(',')
                    lastname=thisauthor[:firstcomma]
                    lastname=lastname.strip()
                    secondcomma=thisauthor.find(',',firstcomma+1)
                    initials=thisauthor[firstcomma:secondcomma]
                    localauthorname=lastname+initials
                    scopuslocalauthorcount+=1
                    if scopuslocalauthorcount==1:
                        scopuslocalauthors=localauthorname
                    else:
                        scopuslocalauthors=scopuslocalauthors+'; '+localauthorname

                start=endauthor+1
                authorcount+=1

            
            #Output Scopus data to dictionary
            if len(scopusdoi)>1 and scopusdoi not in scopusdict:
                scopusdict[scopusdoi]=(scopusauthors,scopusreprintauthor,scopuslocalauthors,scopuslocalauthorcount,scopuslocalreprintauthor,scopuslocalreprintauthoraddress,scopusfunders,scopusfullauthors)


    #doajlist.csv is held in the Input folder
    #it is imported and a dictionary created
    #Download the data from https://doaj.org/csv and rename the file doajlist.csv and place in the Input folder
    #Note April 2018 DOAJ List downloaded from wayback machine https://web.archive.org/web/*/https://doaj.org/csv

    doajfilestring='doajlist2018.csv'

    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    rel_path = "input_files/"+doajfilestring
    abs_file_path2 = os.path.join(script_dir, rel_path)

    doajfile=abs_file_path2

    doajdata=csv.DictReader(open(doajfile,mode="r", encoding="latin-1"))
    for line in doajdata:
        issn1=line['Journal ISSN (print version)']
        issn2=line['Journal EISSN (online version)']
        apc_charged=line['Journal article processing charges (APCs)']
        doaj_apc=line['APC amount']
        doaj_currency=line['Currency']
        doaj_currency=doaj_currency[:3]
        if len(issn1)>0:
            doajdict[issn1]=(apc_charged,doaj_apc,doaj_currency)

        if len(issn2)>0:
            doajdict[issn2]=(apc_charged,doaj_apc,doaj_currency)


    #Function to extract funder data
    def funderout (funder,thislist):

        
        for i,j in unicodereplace:
            funder=funder.replace(i,j)
        if funder[1]!='[':

            if  '[' in funder:
                
                bracket=funder.find('[')-1
                funder=funder[:bracket]
                
            #for i,j in unicodereplace:
                #funder=funder.replace(i,j)
            if funder not in thislist:
                #funder=funder.decode('utf-8')
                funderdata.append((funder,oastatus,potentialaam,potentialpdf))
                thislist.append(funder)
            if funder not in funderlist:
                #funder=funder.decode('utf-8')
                funderlist.append(funder)
            
            return funder, thislist

    #Function to extract subject data
    def subjectout (subject):

        if subject not in subjectlist:
            subjectlist.append(subject)
            subjectdata.append((subject,oastatus,potentialaam,potentialpdf))
        else:
            subjectdata.append((subject,oastatus,potentialaam,potentialpdf))

    #create exchange rates dictionary
    findexchangerates=requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    exchangeratedict=findexchangerates.json()

    #List to turn Sherpa Creative Commons information into standard CC abbreviations
    ccabbrev=[('Creative Commons ','CC'),('Attribution ','-BY'),('Non-Commercial ','-NC'),('Non Commercial ','-NC'),('No Derivatives ','-ND'),('No-Derivatives ','-ND'),('Share Alike ','-SA')]


    #Count the number of records in the input file
    countlines=open(doi_list)

    countlines1= csv.reader(countlines,delimiter=',')

    next(countlines1)
    for line in countlines1:
        
        
    

        check=line[0]
        
        if len(check)>0:
            recordcount+=1

    print(str(recordcount)+' DOIs in file')

    allapcfilestring='allapcs.csv'


    #Import the file of APCs extracted from https://github.com/lmatthia/publisher-oa-portfolios and consolidated
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    rel_path = "input_files/"+allapcfilestring
    abs_file_path2 = os.path.join(script_dir, rel_path)

    allapcfile=abs_file_path2


    allapcs=csv.DictReader(open(allapcfile))

    for line in allapcs:
        allapcissn=line['issn']
        allapctitle=line['journal_title']
        allapc=line['apc']
        allapcissndict[allapcissn]=allapc
        allapctitledict[allapctitle]=allapc
        if '- The' in allapctitle:
            if allapctitle[len(allapctitle)-5:]=='- The':
                shorttitle=allapctitle[:len(allapctitle)-6]
                longtitle='The '+shorttitle
                allapctitledict[shorttitle]=allapc
                allapctitledict[longtitle]=allapc





    nowstart2=datetime.datetime.now()

    records=csv.DictReader(open(doi_list))


    for line in records:
        linecount+=1
        

        print(instita)
        #try:

        #Reset the variables that apply to each row
        #outlist captures all the output data for each row
        outlist=[]
        #counts the number of repositories for this row
        repositorycount=0

        #Variables are cleared.
        
        doi = '';evidence = '';licence = '';oastatus = '';title = '';allauthors = '';numauthors=0;authorcount = 0;morethan20authors = '';scopusauthors = ''
        wosorscopusauthors = '';numberoflocalauthors = '';localauthorlist = '';reprintauthor = '';localreprintauthor = '';reprintauthorislocal = '';journal = ''
        year = '';publisher = '';isoa = '';genre = '';oajournal = '';version = '';host_type = '';greenavailable = '';repout = '';doaj = '';issn = '';inlocalrepository=''
        postarchiving = ''; pdfarchiving = '';colour = '';cclicence = '';citations = '';freetexturl = '';inwos = '';apccharged = '';doajcurrency = '';doajprice = '';
        publishercurrency = '';publisherapc = '';finalapc = '';score = '';msmcount = '';policycount = '';detail = '';funders = '';wossubject = ''; woslocalreprintauthor=''; scopuslocalreprintauthor='';crfunderlist='';potentialaam='';potentialpdf='';issn1='';issn2=''

        #validdoi switches to 'n' if there is a problem and stops execution of the row
        validdoi='y'


        #Import the DOI and remove any spaces, commas etc

        doi=line['DOI']
        doi=doi.replace(' ','')
        doi=doi.replace(',','.')
        lengthdoi=len(doi)
        lastletter=doi[lengthdoi-1:]
        if lastletter=='.':
            doi=doi[:lengthdoi-1]

        #Print and output the DOI
        print(doi)

        retrycount=0
        done='n'
            

            
                
        while done=='n' and retrycount<8:

            try:            
             
                #Set variables to check if the DOI is found in unpaywall.It is sent to search twice
                #the doi will be searched for twice by the unpaywall API before being abandonned
                unpaywallsearch=0
                #unpaywallfound switches to 'y' when the doi is found by the unpaywall API
                unpaywallfound='n'

                print('Checking DOI')

                
                doisearch=requests.get('https://doi.org/api/handles/'+doi,timeout=(10,20))
                doipage=doisearch.content
                doiinfo=str(doipage)
                print('DOI checked')

                if '{"responseCode":1,' not in doiinfo:
                    
                    print('Invalid DOI!')
                    validdoi='n'
                    
                    foute.write('"'+doi+'","Invalid DOI"\n')

                    if inwos=='Yes':

                        try:

                            #title=line['TI']
                            #author=line['AU']
                            title=wosentry[3]
                            authors=wosentry[0]
                            title=title.replace(' ','+')
                            
                            endauthor=author.find(',')
                            author=author[:endauthor]
                            

                            crossreftitledata=requests.get('https://api.crossref.org/works?query.title='+title) #+'&query.author='+author

                            hold=crossreftitledata.content
                            crossreftitledatapage=str(hold)
                            print('Crossref checked by title')
                            


                            published=crossreftitledatapage.find('"published')
                            doistart=crossreftitledatapage.find('"DOI":"',published)+7
                            doiend=crossreftitledatapage.find('"',doistart)

                            doi=crossreftitledatapage[doistart:doiend]
                            


                            doi=doi.replace('\\','')
                            print(doi)


                            validdoi='y'
                        except:
                            errors+=1
                            continue
                print('Requesting Crossref data')
                crossrefdata=requests.get('https://api.crossref.org/works/'+doi,timeout=(10,20))
                

                getpage=crossrefdata.content
                crossrefpage=str(getpage)
                print('Crossref data returned')
                

                

                if 'Resource not found' not in crossrefpage:

                    if 'No server is available to handle this request' in crossrefpage:
                        noserver='y'
                        noservercount=0
                        while noserver=='y' and noservercount<5:

                            print('Waiting for server...')
                            print()
                            time.sleep(60)
                            crossrefdata=requests.get('https://api.crossref.org/works/'+doi,timeout=(10,20))
                            getpage=crossrefdata.content
                            crossrefpage=str(getpage)
                            if 'No server is available to handle this request' not in crossrefpage:
                                noserver='n'
                            else:
                                noservercount+=1

                    year='0000'
                    foundyear='0000'
                    for findyear in findyearlist:
                        
                        if findyear in crossrefpage:
                            beginyear=crossrefpage.find(findyear)+len(findyear)
                            foundyear=crossrefpage[beginyear:beginyear+4]
                                    
                            if int(foundyear)>=startyear and int(foundyear)<=endyear:
                                
                                year=foundyear
                    
                    if year=='0000':
                        year=foundyear
                    
                    print(year)

                    if int(year) >= startyear-2 and int(year) <= endyear+2:

                        while unpaywallsearch<2 and unpaywallfound=='n':

                            print('Requesting Unpaywall data')
                            

                            #Send the DOI to the unpaywall API. 
                            unpaywallfind='https://api.unpaywall.org/v2/'+doi+'?email='+emailaddress

                            
                            
                            findoainfo=requests.get(unpaywallfind,timeout=(10,20))

                            #Read in the output from the API search to a file called oainfo.

                            oapage=findoainfo.content
                            
                            
                            oainfo=str(oapage,encoding='utf-8')


                            print('Unpaywall data returned')
                          
                            
                        
                            
                            

                            




                            #Check for 404 error and increment the counter

                            if 'HTTP_status_code": 404' in oainfo or '"doi":' not in oainfo:

                                unpaywallsearch+=1

                                time.sleep(3)

                            #Change the status to found if it is not a 404
                            else:

                                unpaywallfound='y'





                        #Doublecheck on the incorrect DOIs
                        if unpaywallfound=='n':
                            

                            try:

                                doisearch=requests.get('http://dx.doi.org/'+doi,timeout=(10,20))
                                doipage=doisearch.content
                                doiinfo=str(doipage)


                                if 'This DOI cannot be found ' in doiinfo or '404 Not Found' in doiinfo or 'error-404' in doiinfo:
                                    #doi='Invalid DOI!'
                                    print('Invalid DOI!')
                                    validdoi='n'
                                    outlist.append(doi);outlist.append('Invalid DOI')
                                    errors+=1
                                else:
                                    if validdoi=='y':
                                        outlist.append(doi);outlist.append('Not found in unpaywall')
                                    print('Not found in unpaywall')
                                    validdoi='n'
                                    errors+=1

                                notfound+=1
                            except:

                                print('Not found in unpaywall')
                                validdoi='n'
                                outlist.append(doi);outlist.append('Not found in unpaywall')
                                if validdoi=='y':
                                
                                    foute.write('"'+doi+'","Not found in unpaywall"\n')
                                notfound+=1
                                


                            if 'best_oa_location": null' in oainfo:
                                doi='DOI found but no information!'
                                print('DOI found but no information!')
                                errors+=1
                                outlist.append(doi);outlist.append('No information in unpaywall')
                                validdoi='n'
                                notfound+=1

                            elif '"title": null,' in oainfo:
                                doi='DOI found but no information!'
                                print('DOI found but no information!')
                                errors+=1
                                outlist.append(doi);outlist.append('No information in unpaywalld')
                                validdoi='n'
                                notfound+=1

                            


                            

                        #Continue with the input for unpaywall for valid DOIs. Information on data fields at https://unpaywall.org/data-format

                        else:

                            

                            #Extract evidence - "Used for debugging. Don’t depend on the exact contents of this for anything, because values are subject to change without warning.""
                            if '"evidence": "' not in oainfo:
                                evidence=''
                            else:
                                evidencebegin=oainfo.find('"evidence": "')+13
                                evidenceend=oainfo.find('",',evidencebegin)
                                evidence=oainfo[evidencebegin:evidenceend]

                            if '"license": ' not in oainfo:
                                licence=''
                            else:
                                licencebegin=oainfo.find('"license": ')+12
                                
                                licenceend=oainfo.find('"',licencebegin)
                                
                                licence=oainfo[licencebegin:licenceend]
                            if 'ull,' in licence:
                                licence=''

                            if '"oa_status": "' not in oainfo:
                                oastatus=''
                            else:
                                oastatusbegin=oainfo.find('"oa_status": "')+14
                                oastatusend=oainfo.find('"',oastatusbegin)
                                oastatus=oainfo[oastatusbegin:oastatusend]




                            #Extract the article title
                            if '"title": null,' in oainfo:
                                title=''
                            else:

                                titlebegin=oainfo.find('"title": "')+10
                                titleend=oainfo.find('",',titlebegin)
                                title=oainfo[titlebegin:titleend]

                                #Remove HTML and tabs from title
                                title=re.sub('<.*?>','',title)
                                title=title.replace('\"','')
                                title=title.replace('\t','')

                            
                            
                            for i,j in unicodereplace:
                                title=title.replace(i,j)
                            print(title)

                            

                            #Extract the journal name
                            journalbegin=oainfo.find('journal_name": ')+16
                            statuscheck=oainfo[journalbegin-2:journalbegin+4]
                            #if the resource is not a journal article this will be 'null' in which case a blank is recorded
                            if 'null' in statuscheck:
                                journal=''
                            else:
                                journalend=oainfo.find('",',journalbegin)
                                journal=oainfo[journalbegin:journalend]

                            
                            for i,j in unicodereplace:
                                journal=journal.replace(i,j)
                            
                            #Extract the publisher
                            if '"publisher": "' in oainfo:
                                publisherbegin=oainfo.find('"publisher": "')+14
                                publisherend=oainfo.find('",',publisherbegin)
                                publisher=oainfo[publisherbegin:publisherend]
                                for i,j in unicodereplace:
                                    publisher=publisher.replace(i,j)
                            else:
                                publisher=''
                            
                            

                            #Extract the open access status of the item –this will be either true or false
                            isoabegin=oainfo.find('"is_oa": ')+9
                            isoaend=oainfo.find(',',isoabegin)
                            isoa=oainfo[isoabegin:isoaend]

                            #Update the counts
                            if isoa=='true':
                                truecount+=1


                            

                            #Extract the genre - "Currently the genre is identical to the Crossref-reported type of a given resource. The "journal-article" type is most common, but there are many others."
                            genrebegin=oainfo.find('"genre": "')+10
                            genreend=oainfo.find('",',genrebegin)
                            genre=oainfo[genrebegin:genreend]

                            
                            

                            #Extract the open access status of the journal."Under construction. Included for future compatibility. Will eventually include any fully-OA publication venue, regardless of inclusion in DOAJ"
                            oajournalbegin=oainfo.find('"journal_is_oa": ')+17
                            oajournalend=oainfo.find(',',oajournalbegin)
                            oajournal=oainfo[oajournalbegin:oajournalend]


                            

                            #The unpaywall API
                            #Sent an end point to check the version status from the first section of information about the item on unpaywall. This is the "best version" of the Open Access article
                            datastandard=oainfo.find('"data_standard"')

                            #Extract the version identifier of the "best version". If the atricle is not OA this will be 'null'
                            if '"version": null' in oainfo[:datastandard]:
                                version='null'
                                

                            elif '"version": "' in oainfo:
                                versionbegin=oainfo.find('"version": "')+12
                                versionend=oainfo.find('"',versionbegin)
                                version=oainfo[versionbegin:versionend]

                            
                            else:
                                version=''


                            #Extract the "host type" of the best version – this will be either Publisher or Repository
                            if 'host_type": "' in oainfo:
                                hostbegin=oainfo.find('host_type": "')+13
                                hostend=oainfo.find('",',hostbegin)
                                host_type=oainfo[hostbegin:hostend]

                                
                            else:
                                host_type=''



                            


                            #The next section captures all the repository data for this row item. Because there may be several repositories the process loops
                            #'pmh_id": "oai' indicates an item in a repository. As there may be several of these this section of the program loops until no further repositories are found
                            #host_type=''
                            #if 'pmh_id": "oai'  in oainfo:
                            if '"has_repository_copy": true' in oainfo:
                                greenavailable='Yes'
                                


                                #skip represents the start of the data after the best version. This is to avoid double counting. Oainfohold is the truncated version of the unpaywall page which excludes repository data already found
                                skip=oainfo.find('"data_standard"')
                                oainfohold=oainfo[skip:]


                                #Loop until all repositories have been found
                                while '"pmh_id": "oai:' in oainfohold:




                                    #Extract the repository address
                                    pmhbegin=oainfohold.find('"pmh_id": "oai:')+15
                                    
                                    pmhend=oainfohold.find(':',pmhbegin)
                                    #Check for dashes in the repository address which will cause a malfunction
                                    pmhdash=oainfohold.find('/',pmhbegin)
                                    if pmhdash<pmhend:
                                        pmhend=pmhdash

                                


                                    pmh=oainfohold[pmhbegin:pmhend]

                                    


                                    #Check for presence of  repository in repout

                                    if pmh not in repout:
                                        


                                        #Check for line ending to show the end of the repository name
                                        if('\\n') in pmh:
                                            pmhend=oainfohold.find('\\n',pmhbegin)-2
                                            pmh=oainfohold[pmhbegin:pmhend]

                                        #Keep to see if this repository is already in the repository list and if not add it to the list

                                        if pmh not in repositorylist and len(pmh)>0:
                                            repositorylist.append(pmh)

                                        #Identify the version for this instance
                                        if '"version": null' in oainfohold:
                                            pmhversion='null'
                                        else:

                                            versionbegin=oainfohold.find('"version": "')+12
                                            versionend=oainfohold.find('"',versionbegin)
                                            pmhversion=oainfohold[versionbegin:versionend]

                                        
                                        #pmhlist records data for each instance of an item in a repository
                                        pmhlist.append((doi,pmh,pmhversion))
                                        #






                                        #repout records all the repositories in which this item is held
                                        repout=repout+pmh+' '
                                        
                                        

                                        repositorycount+=1
                                        

                                    #Moves on to the next repository for this item. The 'evidence' tag identifies the beginning of the next repository set of repository data
                                    next=oainfohold.find('"evidence"',pmhend+10)
                                    oainfohold=oainfohold[next:]

                            else:
                                greenavailable='No'
                            #In rare cases the tag "pmh_id": "oai: is not present although the item is held in a repository
                            if host_type=='repository' and repositorycount==0:
                                repout='no_oai_data'
                                repositorycount=1

                            if greenavailable=='Yes' and repstring in repout and len(repstring)>5:
                                inlocalrepository='Yes'
                            else:
                                inlocalrepository='No'
                            print('In local repository = '+inlocalrepository)
                                    

                            
                            #Check to see if journal is in DOAJ. The responses will be TRUE or FALSE
                            doajbegin=oainfo.find('"journal_is_in_doaj": ')+22
                            doajend=oainfo.find(',',doajbegin)
                            doaj=oainfo[doajbegin:doajend]

                        

                            #Check for URL for OA Items
                            if '"url_for_pdf":' in oainfo and '"url_for_pdf": null' not in oainfo:
                                urlbegin=oainfo.find('"url_for_pdf": ')+16
                                urlend=oainfo.find('"',urlbegin)
                                freetexturl=oainfo[urlbegin:urlend]

                            elif '"free_fulltext_url": ' in oainfo:
                                urlbegin=oainfo.find('"free_fulltext_url": ')+23
                                urlend=oainfo.find('"',urlbegin)
                                freetexturl=oainfo[urlbegin:urlend]

                            elif '"url_for_landing_page": ' in oainfo:
                                urlbegin=oainfo.find('"url_for_landing_page": ')+25
                                urlend=oainfo.find('"',urlbegin)
                                freetexturl=oainfo[urlbegin:urlend]

                            #elif

                            else:
                                freetexturl=''

                            #Identify ISSNs. If there is more than one they will come out as a single string using a comma to separate

                            issnlist=[]
                            issnbegin=oainfo.find('"journal_issns":')+18
                            if oainfo[issnbegin-1:issnbegin+3]=='null':
                                issn1='null'
                                issn2=''
                            else:
                                issnend=oainfo.find('",',issnbegin)
                                issnentry=oainfo[issnbegin:issnend]

                                issn1=issnentry[0:9]
                                
                                print(issn1)
                               
                                #print(issnentry)
                                #print('issn='+issn1)
                                if len(issnentry)>10:
                                    
                                    
                                    issn2=issnentry[10:19]
                                    print(issn2)
                                    

                                    
                                else:
                                    
                                    #Create a list of the ISSNs for this journal
                                    if issn1!='null':
                                        
                                        

                                        if issn1 in crossrefissndict:
                                            
                                            
                                            
                                            issncrentry=crossrefissndict.get(issn1)
                                            issn2=issncrentry
                                            
                                            if issncrentry=='':
                                                issn2=''

                                        else:


                                
                                            print('Requesting Crossref journal data')
                                            issn2search='https://api.crossref.org/journals/'+issn1
                                            
                                            getissn2=requests.get(issn2search,timeout=(10,20))
                                            crossrefjournaldata=str(getissn2.content)
                                            #print(crossrefjournaldata)

                                            if 'Resource not found'not in crossrefjournaldata:
                                            
                                                issnstart=crossrefjournaldata.find('"ISSN":[')+8
                                                issnend=crossrefjournaldata.find(']',issnstart)
                                                allissns=crossrefjournaldata[issnstart:issnend]
                                                
                                                if ',' in allissns:
                                                    firstissn=allissns[1:10]
                                                    secondissn=allissns[13:22]
                                                    
                                                    if issn==firstissn:
                                                        issn2=secondissn
                                                    else:
                                                        issn2=firstissn                           
                                                
                                                
                                                    
                                            else:
                                                issn2=''
                                       
                                
                                if len(issn2)==9:
                                    crossrefissndict[issn1]=issn2 
                                    crossrefissndict[issn2]=issn1
                                elif len(issn2)==0:
                                    crossrefissndict[issn1]=''
                                issnlist.append(issn1)
                                if len(issn2)>1 and issn2!=issn1:
                                    
                                    issnlist.append(issn2)
                                
                            
                            

                            #Use these ISSNs to check the DOAJ data for an APC currency and amount
                            #Set variables
                            apccharged=''
                            doajcurrency=''
                            doajprice=''


                            if genre=='journal-article':
                                #Do for each ISSN

                                for issn in issnlist:

                                    if issn in doajdict:

                                        doajentry=doajdict.get(issn)

                                        doajcurrency=doajentry[2]
                                        doajprice=doajentry[1]
                                        apccharged=doajentry[0]
                                        doaj='TRUE'





                            


                            if oastatus=='gold' and doaj=='TRUE' and apccharged=='No':
                                oastatus='diamond'

                            print('oastatus = '+oastatus)




                            #Move to Sherpa/Romeo website to gather data on the OA allowances for this journal
                            #Reset variables for this item

                            postarchiving=''
                            pdfarchiving=''
                            colour=''
                            sherpafound='n'
                            cclicence=''
                            update=''
                            sherpasearchcount=0

                            print(journal)
                            
                            print(issn)
                            
                            
                            if len(issn)>6:
                                
                                
                                
                                for issn in issnlist:

                                    
                                    
                                    
                                    
                                    
                                    if sherpafound=='n':
                                        
                                        
                                        
                                        postarchiving=''
                                        pdfarchiving=''
                                        colour=''
                                        cclicence=''
                                        update=''
                                        



                                        

                                        if issn in sherpadict:
                                            
                                        
                                            
                                            
                                            sherpaentry=sherpadict.get(issn)
                                            

                                            if len(sherpaentry[0])>0:

                                            
                                                postarchiving=sherpaentry[0]
                                                
                                                pdfarchiving=sherpaentry[1]
                                                
                                                colour=sherpaentry[2]
                                            
                                                cclicence=sherpaentry[3]

                                                update=sherpaentry[5]

                                            
                                            
                                                sherpafound='y'
                                            

                                        
                                        else:
                                            

                                            #Send ISSN request to the Sherpa/Romeo API. If the ISSN is not found then each item as output as No Information. Details of the Sherpa/Romeo API can be found at – http://www.sherpa.ac.uk/romeo/SHERPA%20RoMEO%20API%20V-2-9%202013-11-25.pdf
                                            notinsherpacount+=1
                                            
                                            print('Requesting Sherpa/Romeo data')

                                            sherpasearchstring='http://www.sherpa.ac.uk/romeo/api29.php?issn='+issn+'&ak='+sherpakey
                                            
                                            

                                            sherpasearch=requests.get(sherpasearchstring,timeout=(10,20))

                                            
                                            
                                            sherpapage=sherpasearch.content
                                            sherpainfo=str(sherpapage)

                                            print('Sherpa/Romeo data returned')
                                            
                                            
                                            
                                            #If the ISSN is found in Sherpa/Romeo it will not be searched for again
                                            if '<numhits>' in sherpainfo and 'numhits>0<' not in sherpainfo:
                                                sherpafound='y'

                                            if sherpafound=='y':
                                                #Postarchiving is a tag that identifies what can be done with an Accepted Manuscript
                                                postarchivingstart=sherpainfo.find('postarchiving>')+14; postarchivingend=sherpainfo.find('<',postarchivingstart)
                                                postarchiving=sherpainfo[postarchivingstart:postarchivingend]

                                                if postarchiving =='can' and '<postrestrictions />' in sherpainfo and '&lt;num&gt;' in sherpainfo:

                                                    postarchivingstart=sherpainfo.find('&lt;num&gt;')+11
                                                    postarchivingend=sherpainfo.find('&',postarchivingstart)
                                                    postarchiving=sherpainfo[postarchivingstart:postarchivingend]
                                                    unitstart=sherpainfo.find('&quot;&gt;',postarchivingend)+10
                                                    unitend=sherpainfo.find('&',unitstart)
                                                    unit=sherpainfo[unitstart:unitend]
                                                    postarchiving=postarchiving+' '+unit+' embargo'




                                                #If postarchiving is restricted, identify the restrictions
                                                if postarchiving=='restricted' and 'media embargo' not in sherpainfo:
                                                    #Post archiving embargo restriction periods are generally identified by the tags <num> and </num>. If these are not present then take the whole postrestriction information
                                                    if 'postrestriction>&lt;num&gt;' not in sherpainfo:
                                                        postrestrictionstart=sherpainfo.find('<postrestriction>')+17
                                                        postrestrictionend=sherpainfo.find('</',postrestrictionstart)
                                                        postarchiving=sherpainfo[postrestrictionstart:postrestrictionend]
                                                    #Otherwise identify the numerical value between the tags
                                                    else:
                                                        postrestrictionstart=sherpainfo.find('postrestriction>&lt;num&gt;')+27; postrestrictionend=sherpainfo.find('&',postrestrictionstart)
                                                        postrestriction=sherpainfo[postrestrictionstart:postrestrictionend]

                                                        #Now identify the unit which will be either months or years
                                                        unitstart=sherpainfo.find(';&gt;',postrestrictionend)+5; unitend=sherpainfo.find('&',unitstart)

                                                        unit=sherpainfo[unitstart:unitend]

                                                        postarchiving=postrestriction+' '+unit+' embargo'

                                                #Identify items with media embargoes
                                                if postarchiving=='restricted' and'media embargo' in sherpainfo:
                                                    postarchiving='after media embargo'



                                                #Items that have not been found or that have no postarchiving information will give the value 13 for postarchiving start. This is because the value -1 is given when something is not found in this has been added to the number 14
                                                if postarchivingstart==13:
                                                    postarchiving='No information'

                                                if sherpainfo.count('Creative Commons')>1:
                                                    startlicencesearch=sherpainfo.find('<condition>')
                                                    cclicencestart=sherpainfo.find('Creative Commons ',startlicencesearch)
                                                    cclicenceend=sherpainfo.find('icen',cclicencestart)-1
                                                    cclicence=sherpainfo[cclicencestart:cclicenceend]

                                                    for i,j in ccabbrev:

                                                        cclicence2=cclicence.replace(i,j)
                                                        cclicence=cclicence2
                                                    



                                                #A similar process is followed for PDF archiving. This is when the publisher's version is able to be used in a repository.
                                                pdfarchivingstart=sherpainfo.find('pdfarchiving>')+13; pdfarchivingend=sherpainfo.find('<',pdfarchivingstart)
                                                pdfarchiving=sherpainfo[pdfarchivingstart:pdfarchivingend]
                                                if pdfarchivingstart==12:
                                                    pdfarchiving='No information'
                                                elif pdfarchiving=='restricted' and 'version/PDF may be used' in sherpainfo and 'embargo' in sherpainfo[pdfarchivingstart:]:
                                                    embargosnipstart=sherpainfo.find('version/PDF may be used')
                                                    embargosnipend=sherpainfo.find('embargo',embargosnipstart)
                                                    embargosnip=sherpainfo[embargosnipstart:embargosnipend]
                                                    embargonumberstart=embargosnip.find('num&gt;')+7
                                                    embargonumberend=embargosnip.find('&',embargonumberstart)
                                                    embargonumber=embargosnip[embargonumberstart:embargonumberend]
                                                    unitstart=embargosnip.find(';&gt;')+5
                                                    unitend=embargosnip.find('&',unitstart)
                                                    unit=embargosnip[unitstart:unitend]
                                                    pdfarchiving=embargonumber+' '+unit+' embargo'
                                                elif pdfarchiving=='restricted' and 'version/PDF may be used' in sherpainfo and 'after publication' in sherpainfo[pdfarchivingstart:]:
                                                    embargostart=sherpainfo.find('version/PDF may be used',pdfarchivingstart)+24
                                                    embargoend=sherpainfo.find('after publication')
                                                    pdfarchiving=sherpainfo[embargostart:embargoend]+'embargo'
                                                elif pdfarchiving=='restricted' and 'version/PDF may be used' in sherpainfo and 'embargo from the date of publication' in sherpainfo[pdfarchivingstart:]:
                                                    embargostart=sherpainfo.find('after a ',pdfarchivingstart)+8
                                                    embargoend=sherpainfo.find('embargo from the date of publication')
                                                    pdfarchiving=sherpainfo[embargostart:embargoend]+'embargo'


                                                elif pdfarchiving=='restricted' and '<pdfrestriction>' in sherpainfo and 'embargo' in sherpainfo[pdfarchivingstart:]:
                                                    restrictionstart=sherpainfo.find('<pdfrestriction>')
                                                    restrictionend=sherpainfo.find('</pdfrestrictions')
                                                    pdfrestriction=sherpainfo[restrictionstart:restrictionend]
                                                    numberstart=pdfrestriction.find('num&gt;')+7
                                                    numberend=pdfrestriction.find('&',numberstart)
                                                    number=pdfrestriction[numberstart:numberend]
                                                    unitstart=pdfrestriction.find(';&gt;')+5
                                                    unitend=pdfrestriction.find('&',unitstart)
                                                    unit=pdfrestriction[unitstart:unitend]

                                                    pdfarchiving=number+' '+unit+' embargo'

                                                elif pdfarchiving=='restricted' and '<pdfrestriction>' in sherpainfo and 'media embargo' in sherpainfo[pdfarchivingstart:]:
                                                    pdfarchiving='after media embargo'

                                                #Is the restriction conditions  are more than 20 characters in length then the tag "Special conditions apply" is given to the item
                                                if len(pdfarchiving)>20:
                                                    pdfarchiving='Special conditions apply'

                                                #The Sherpa/Romeo colour is extracted
                                                colourstart=sherpainfo.find('colour>')+7;colourend=sherpainfo.find('<',colourstart)
                                                colour=sherpainfo[colourstart:colourend]
                                                if colourstart==6:
                                                    colour='No information'

                                                #The update date is extracted
                                                updatestart=sherpainfo.find('<dateupdated>')+13;updateend=sherpainfo.find(' ',updatestart)
                                                update=sherpainfo[updatestart:updateend]
                                                if updatestart==12:
                                                    update=''

                                                #"No information" reported when ISSN not found in Sherpa/Romeo
                                                if sherpafound=='n' and sherpasearchcount==2:
                                                    postarchiving='No information';pdfarchiving='No information';colour='No information'
                                       
                                            else:
                                                sherpadict[issn]=(postarchiving,pdfarchiving,colour,cclicence,journal,update)   

                                    sherpadict[issn]=(postarchiving,pdfarchiving,colour,cclicence,journal,update)
                                
                                       
                                                
                                potentialaam=''
                                if oastatus=='closed':
                                    if postarchiving=='can':
                                        potentialaam='y'
                                    elif 'embargo' in postarchiving:
                                        potentialaam='e'
                                
                                potentialpdf=''
                                if oastatus=='closed':
                                    if pdfarchiving=='can':
                                        potentialpdf='y'
                                    elif 'embargo' in pdfarchiving:
                                        potentialpdf='e'
                            else:
                                print('No issn')    
                            

                        
                            if wosused == 'Yes':

                                if doi in wosdict:
                                    inwos='Yes'

                                    wosentry=wosdict.get(doi)
                                    
                                    
                                    
                                    wosauthors=wosentry[0] 
                                    woslocalauthorlist=wosentry[1]
                                    numberofwoslocalauthors=wosentry[2]
                                    wosreprintauthor=wosentry[3]
                                    woslocalreprintauthor=wosentry[4]
                                    woslocalreprintauthoraddress=wosentry[5]
                                    wostitle=wosentry[6]
                                    wossubject=wosentry[7]
                                    wosfunder=wosentry[8]
                                    

                                else:
                                    wosauthors=''; woslocalauthorlist=''
                                    numberofwoslocalauthors=''
                                    wosreprintauthor=''
                                    woslocalreprintauthor=''
                                    wostitle=''
                                    wossubject=''
                                    wosfunder=''
                                    inwos='No'

                                
                            else:
                                wosauthors=''
                                woslocalauthorlist=''
                                numberofwoslocalauthors=''
                                wosreprintauthor=''
                                woslocalreprintauthor=''
                                wostitle=''
                                wossubject=''
                                wosfunder=''
                                inwos='No'
                            
                            if scopusused=='Yes':
                                if doi in scopusdict:
                                    
                                    scopusentry=scopusdict.get(doi)
                                    
                                    
                                    
                                    
                                    scopusauthors=scopusentry[0]  
                                    scopusreprintauthor=scopusentry[1]  
                                    scopuslocalauthors=scopusentry[2]  
                                    scopuslocalauthorcount=scopusentry[3]
                                    scopuslocalreprintauthor=scopusentry[4]
                                    scopuslocalreprintauthoraddress=scopusentry[5]
                                    scopusfunders=scopusentry[6]
                                   
                                    scopusfullauthors=scopusentry[7]
                                
                                else:
                                    scopusauthors=''
                                    scopusfullauthors=''
                                    scopusreprintauthor='' 
                                    scopuslocalauthors=''  
                                    scopuslocalauthorcount=''
                                    scopuslocalreprintauthor=''
                                    scopusfunders=''
                            else:
                                scopusauthors=''
                                scopusfullauthors=''
                                scopusreprintauthor='' 
                                scopuslocalauthors=''  
                                scopuslocalauthorcount=''
                                scopuslocalreprintauthor=''
                                scopusfunders=''
                                        

                                
                            
                            
                            
                            wosorscopusauthors=wosauthors+' '+scopusfullauthors
                            wosorscopusauthors=wosorscopusauthors[:10000]
                            
                        
                            
                            
                            

                            if woslocalauthorlist=='':
                                
                                if scopuslocalauthors=='':
                                    
                                    localauthorlist=''
                                else:
                                    
                                    localauthorlist=scopuslocalauthors
                                    
                            else:
                                localauthorlist=woslocalauthorlist

                            

                            if numberofwoslocalauthors=='':
                                if scopuslocalauthorcount=='':
                                    numberoflocalauthors=''
                                else:
                                    numberoflocalauthors=scopuslocalauthorcount
                            else:
                                numberoflocalauthors=numberofwoslocalauthors

                            if wosreprintauthor=='':
                                if scopusreprintauthor=='':
                                    reprintauthor=''
                                else:
                                    reprintauthor=scopusreprintauthor
                            else:
                                reprintauthor=wosreprintauthor

                            if woslocalreprintauthor=='':
                                if scopuslocalreprintauthor=='':
                                    localreprintauthor=''
                                else:
                                    localreprintauthor=scopuslocalreprintauthor
                            else:
                                localreprintauthor=woslocalreprintauthor

                            
                            
                            if inwos=='Yes':
                                localreprintauthoraddress=woslocalreprintauthoraddress

                            elif doi in scopusdict:
                                localreprintauthoraddress=scopuslocalreprintauthoraddress

                            
                            else:
                                localreprintauthoraddress=''

                            thislist=[]

                            funders=''
                            
                            
                        
                            if len(wosfunder)>0:
                                
                                countfunders=wosfunder.count('; ')+1
                                
                                if '"' in wosfunder:
                                    wosfunder=wosfunder.replace('"','')
                                    #funders=wosfunder.count('; ')+1
                                for i,j in unicodereplace                            :
                                    wosfunder=wosfunder.replace(i,j)
                                fundercount=0
                                start=0
                                if countfunders==1:
                                    funder=wosfunder


                                    funderout(funder,thislist)


                                else:


                                    while fundercount<countfunders:

                                        


                                        semicolon=wosfunder.find('; ',start)

                                        if semicolon!=-1:
                                            if countfunders==1:
                                                funder=wosfunder


                                                funderout(funder,thislist)



                                            if fundercount==0:

                                                funder=wosfunder[start:semicolon]


                                                funderout(funder,thislist)




                                            else:

                                                funder=wosfunder[start+1:semicolon]

                                                funderout(funder,thislist)

                                            start=semicolon+1
                                            fundercount+=1

                                        else:
                                            funder=wosfunder[start+1:]

                                            funderout(funder,thislist)


                                            start=semicolon+1
                                
                                            fundercount+=1
                            
                            elif len(scopusfunders)>0:
                                
                                
                                countfunders=scopusfunders.count('; ')+1
                                
                                if '"' in scopusfunders:
                                    scopusfunders=scopusfunders.replace('"','')
                                    
                                fundercount=0
                                start=0
                                if countfunders==1:
                                    funder=scopusfunders


                                    funderout(funder,thislist)


                                else:


                                    while fundercount<countfunders:

                                        


                                        semicolon=scopusfunders.find('; ',start)

                                        if semicolon!=-1:
                                            if countfunders==1:
                                                funder=scopusfunders


                                                funderout(funder,thislist)



                                            if fundercount==0:

                                                funder=scopusfunders[start:semicolon]
                                                funder=funder.replace(u'\\xa0',' ')

                                                

                                                funderout(funder,thislist)




                                            else:

                                                funder=scopusfunders[start+1:semicolon]

                                                funderout(funder,thislist)

                                            start=semicolon+1
                                            fundercount+=1

                                        else:
                                            funder=scopusfunders[start+1:]

                                            funderout(funder,thislist)


                                            start=semicolon+1
                                
                                            fundercount+=1
                                                   

                                    if len(thislist)>0:
                                            

                                                funders=str(thislist)
                                                funders=funders.replace('[','')
                                                funders=funders.replace(']','')
                                                funders=funders.replace(',',';')
                                                funders=funders.replace('\'','')
                                                
                                                for i,j in unicodereplace:
                                                    funders=funders.replace(i,j)

                                        

                            else:
                                funders = ''

                            

                                            
                                    
                            if funders=='':
                                funders=scopusfunders
                            
                            

                            if '"' in wossubject:

                                wossubject=wossubject.replace('"','')

                            countsubjects=wossubject.count('; ')+1

                            subjectcount=0
                            start=0

                            if len(wossubject)==0:
                                countsubjects=0
                            
                            
                            

                            elif countsubjects==1:
                                subject=wossubject



                                subjectout(subject)


                            else:



                                while subjectcount<countsubjects:



                                    semicolon=wossubject.find('; ',start)

                                    if semicolon!=-1:
                                        if countsubjects==1:
                                            subject=wossubject

                                            
                                            subjectout(subject)



                                        if subjectcount==0:

                                            subject=wossubject[start:semicolon]


                                            subjectout(subject)
                                            




                                        else:

                                            subject=wossubject[start+1:semicolon]

                                            subjectout(subject)
                                            

                                        start=semicolon+1
                                        subjectcount+=1

                                    else:
                                        subject=wossubject[start+1:]

                                        subjectout(subject)
                                        


                                        start=semicolon+1
                                        subjectcount+=1

                            
                            if instita in wosauthors:
                                numberoflocaldepts=wosauthors.count(instita)
                                
                                start=0
                                tempdepartmentlist=[]
                                for i in range(0,numberoflocaldepts):
                                    department=''
                                    startdept=wosauthors.find(instita,start)
                                    firstcomma=wosauthors.find(',',startdept)
                                    secondcomma=wosauthors.find(',',firstcomma+1)
                                    department=wosauthors[startdept:secondcomma]

                                    if len(department)>0:                    
                                        if department not in tempdepartmentlist:
                                            tempdepartmentlist.append(department)
                                        if department not in departmentlist:
                                            departmentlist.append(department)
                                    start=secondcomma
                                    

                                
                                for department in tempdepartmentlist:
                                    
                                    departmentdata.append((department,oastatus,potentialaam,potentialpdf))
                            
                            if scopusinstnamea in scopusfullauthors:
                                
                                tempdepartmentlist=[]
                                numberofauthors=scopusfullauthors.count(';')+1
                                
                                start=0
                                startauthor=0
                                for i in range(0,numberofauthors):
                                    department=''
                                    endauthor=scopusfullauthors.find(';',startauthor)
                                    allauthor=scopusfullauthors[startauthor:endauthor]
                                    
                                    
                                    if scopusinstnamea in allauthor:
                                        
                                        startdepartment=allauthor.find('.,')+3
                                        
                                        enddepartment=allauthor.find(scopusinstnamea)+len(scopusinstnamea)
                                        
                                        department=allauthor[startdepartment:enddepartment]
                                                                
                                    startauthor=endauthor+1
                                    if len(department)>0:
                                        if department not in tempdepartmentlist:
                                            tempdepartmentlist.append(department)
                                        if department not in departmentlist:
                                            departmentlist.append(department)
                                    

                                for department in tempdepartmentlist:
                                    
                                    departmentdata.append((department,oastatus,potentialaam,potentialpdf))
                        
                            #Check Crossref for citations of the item identified by its DOI
                            
                            if validdoi=='y':
                                
                                

                                if '"is-referenced-by-count":' in crossrefpage:
                                    refstart=crossrefpage.find('"is-referenced-by-count":')+25
                                    refend=crossrefpage.find(',',refstart)
                                    citations=crossrefpage[refstart:refend]
                                elif 'Resource not found' in crossrefpage:
                                    citations=''
                                else:
                                    citations='0'


                                allauthors=''
                                if '"given":"'in crossrefpage:

                                    numauthors=crossrefpage.count('"given":"')
                                    authorcount=str(numauthors)

                                    nextauthor=0
                                    familyend=1
                                    

                                    while nextauthor<numauthors and nextauthor<21:

                                        givenstart=crossrefpage.find('"given":"',familyend)+9

                                        givenend=crossrefpage.find('"',givenstart)

                                        given=crossrefpage[givenstart:givenend]
                                       

                                        familystart=crossrefpage.find('"family":"',givenend)+10
                                        familyend=crossrefpage.find('"',familystart)
                                        family=crossrefpage[familystart:familyend]
                                       
                                        authorname=family+', '+given

                                        if '"affiliation":[{"name":"' in crossrefpage[familyend:]:
                                            startaffil= crossrefpage.find('"affiliation":[{"name":"',familyend)+24
                                            endaffil=crossrefpage.find('"}]',startaffil)
                                            affil=crossrefpage[startaffil:endaffil]
                                            if '"},{"name":"' in affil:
                                                affil = affil.replace('"},{"name":"',', ')
                                            
                                            affil=': '+affil
                                        else:
                                            affil=''
                                        authorname=authorname+affil
                                        
                                        if nextauthor==0:
                                            allauthors=authorname
                                        else:
                                            allauthors=allauthors+'; '+authorname
                                        nextauthor+=1

                                elif 'author":[{"name":"' in crossrefpage:


                                    nextauthor=0
                                    start=crossrefpage.find('author":[{"name":"')

                                    numauthors=crossrefpage.count('"name":',start)
                                    authorcount=str(numauthors)
                                    allauthors=''

                                    while nextauthor<numauthors and nextauthor<21:

                                        namestart=crossrefpage.find('"name":',start)+8
                                        nameend=crossrefpage.find('"',namestart)
                                        authorname=crossrefpage[namestart:nameend]

                                        if '"affiliation":[{"name":"' in crossrefpage[nameend:]:
                                            startaffil= crossrefpage.find('"affiliation":[{"name":"',familyend)+24
                                            endaffil=crossrefpage.find('"}]',startaffil)
                                            affil=crossrefpage[startaffil:endaffil]
                                            if '"},{"name":"' in affil:
                                                affil = affil.replace('"},{"name":"',', ')
                                            
                                            affil=': '+affil
                                        else:
                                            affil=''
                                        authorname=authorname+affil
                                        
                                        
                                        start=nameend
                                        if nextauthor==0:
                                            allauthors=authorname
                                        else:
                                            allauthors=allauthors+'; '+authorname
                                        nextauthor+=1

                                elif 'author":[{"family":"'in crossrefpage:


                                    nextauthor=0
                                    start=crossrefpage.find('author":[{"family":"')

                                    numauthors=crossrefpage.count('"family":"',start)
                                    authorcount=str(numauthors)
                                    allauthors=''

                                    while nextauthor<numauthors and nextauthor<21:

                                        namestart=crossrefpage.find('"family":"',start)+10
                                        nameend=crossrefpage.find('"',namestart)
                                        authorname=crossrefpage[namestart:nameend]

                                        if '"affiliation":[{"name":"' in crossrefpage[nameend:]:
                                            startaffil= crossrefpage.find('"affiliation":[{"name":"',familyend)+24
                                            endaffil=crossrefpage.find('"}]',startaffil)
                                            affil=crossrefpage[startaffil:endaffil]
                                            if '"},{"name":"' in affil:
                                                affil = affil.replace('"},{"name":"',', ')
                                            
                                            affil=': '+affil
                                        else:
                                            affil=''
                                        authorname=authorname+affil
                                        
                                        
                                        start=nameend
                                        if nextauthor==0:
                                            allauthors=authorname
                                        else:
                                            allauthors=allauthors+'; '+authorname
                                        nextauthor+=1






                                else:
                                    #correspond_author=''
                                    allauthors=''

                                    authorcount=''

                            
                            
                            if '\\u' in allauthors :
                                
                                for i,j in unicodereplace:
                                    
                                    allauthors2=allauthors.replace(i,j)
                                    allauthors=allauthors2
                            allauthors=allauthors.replace('\\','')
                            
                           
                            if '"funder":[{' in crossrefpage:
                                fundercount=0
                                funderstart=0
                                crfunderlist=''
                                startcrfunderdata=crossrefpage.find('"funder":[{')+11
                                endcrfunderdata=crossrefpage.find(']}],')
                                crfunderdata=crossrefpage[startcrfunderdata:endcrfunderdata]
                                numberofcrfunders=crfunderdata.count('"name":"')
                                while fundercount<numberofcrfunders:
                                    startcrfunder=crfunderdata.find('"name":"',funderstart)+8
                                    endcrfunder=crfunderdata.find('"',startcrfunder)
                                    crfunder=crfunderdata[startcrfunder:endcrfunder]
                                    
                                    funderstart=endcrfunder
                                    fundercount+=1
                                    if fundercount==1:
                                        crfunderlist=crfunder
                                    else:
                                        crfunderlist=crfunderlist+'; '+crfunder

                            else:
                                crfunder=''

                            if '\\u' in crfunderlist:
                                for i,j in unicodereplace:
                                    crfunderlist2=crfunderlist.replace(i,j)
                                    crfunderlist=crfunderlist2

                            crfunderlist=crfunderlist.replace('\\','')
                            
                            
                            
                            
                            
                            #for issn in issnlist:
                           
                            if len(issnlist)>0:
                                if issnlist[0] in allapcissndict:
                                    
                                    publishercurrency='USD'
                                    publisherapc=allapcissndict.get(issnlist[0])

                                elif len(issnlist)==2 and issnlist[1] in allapcissndict:
                                    
                                    publishercurrency='USD'
                                    publisherapc=allapcissndict.get(issnlist[1])    
                                

                                elif  journal in allapctitledict:
                                    
                                    publishercurrency='USD'
                                    publisherapc=allapctitledict.get(journal)

                                
                                elif 'American Physical Society (APS)' in publisher:
                                    if 'Physical Review Letters' in journal:
                                        publishercurrency='USD'
                                        publisherapc='3500'
                                    elif 'Physical Review Applied' in journal:
                                        publishercurrency='USD'
                                        publisherapc='2500'
                                    elif 'Physical Review X' in journal:
                                        publishercurrency='USD'
                                        publisherapc='4000'
                                    elif 'Physical Review Physics Education Research' in journal:
                                        publishercurrency='USD'
                                        publisherapc='2000'
                                    elif 'Physical Review' in journal:
                                        publishercurrency='USD'
                                        publisherapc='2200'
                                    else:
                                        publishercurrency=''
                                        publisherapc=''

                                elif 'Emerald' in publisher:
                                    publishercurrency='USD'
                                    publisherapc='3240'

                                elif 'American Society for Microbiology' in publisher:
                                    if 'Microbiology Resource Announcements' in journal:
                                        publishercurrency='USD'
                                        publisherapc='1000'
                                    elif 'Journal of Microbiology & Biology Education' in journal or 'Microbiology and Molecular Biology Reviews' in journal:
                                        publishercurrency='USD'
                                        publisherapc='0'
                                    
                                    else:
                                        publishercurrency='USD'
                                        publisherapc='3500'

                                elif 'Royal Society of Chemistry' in publisher:
                                    publishercurrency='GBP'
                                    publisherapc='1600'

                                elif 'American Chemical Society' in publisher:
                                    publishercurrency='USD'
                                    publisherapc='4000'

                                elif 'CSIRO Publishing' in publisher:
                                    publishercurrency='USD'
                                    publisherapc='2700'

                                elif 'Institute of Electrical and Electronics Engineers' in publisher:
                                    publishercurrency='USD'
                                    if journal=='IEEE Access':
                                        publisherapc='1750'
                                    else:
                                        publisherapc='2045'


                            else:
                                publishercurrency=''
                                publisherapc=''

                            
                            if apccharged=='No':
                                finalapc='0'

                            elif len(publishercurrency)>2:

                                
                                finalcurrency=exchangeratedict['rates'][publishercurrency]

                                
                                finalapc=str(int(publisherapc)/finalcurrency)

                                if '.' in finalapc:
                                    finddot=finalapc.find('.')
                                    finalapc=finalapc[:finddot]

                            elif len(doajcurrency)>2:

                                
                                finalcurrency=exchangeratedict['rates'][doajcurrency]

                                finalapc=str(int(doajprice)/finalcurrency)

                                if '.' in finalapc:
                                    finddot=finalapc.find('.')
                                    finalapc=finalapc[:finddot]
                                
                            
                                
                            

                            else:
                                finalapc=''

                                                
                            
                            
                            
                            
                            numberoflocalauthors=str(numberoflocalauthors)
                        
                            


                        
                            if numauthors>20:
                                morethan20authors='Yes'
                            else:
                                morethan20authors='No'
                                
                            
                            if len(localreprintauthor)>1:
                                reprintauthorislocal='Yes'
                            else:
                                reprintauthorislocal='No'

                            
                            
                            #Send the DOI to the altmetric API. 
                            print('Requesting Altmetric data')
                            findaltm=requests.get('https://api.altmetric.com/v1/doi/'+doi,timeout=(10,20))

                            #Read in the output from the API search to a page called altminfo.

                            altmpage=findaltm.content
                            altminfo=str(altmpage,encoding='utf-8')
                            for i,j in unicodereplace:
                                altminfo=altminfo.replace(i,j)
                            #altminfo=codecs.decode(altminfo,'unicode-escape')

                            print('Altmetric data returned')
                            if '"score":' in altminfo:

                                startscore=altminfo.find('"score":')+8
                                endscore=altminfo.find(',',startscore)
                                score=altminfo[startscore:endscore]
                            else:
                                score='0'

                            if '"cited_by_msm_count":' in altminfo:
                                msmstart=altminfo.find('"cited_by_msm_count":')+21
                                msmend=altminfo.find(',',msmstart)
                                msmcount=altminfo[msmstart:msmend]
                            else:
                                msmcount='0'


                            if '"cited_by_policies_count":' in altminfo:
                                policystart=altminfo.find('"cited_by_policies_count":')+26
                                policyend=altminfo.find(',',policystart)
                                policycount=altminfo[policystart:policyend]
                            else:
                                policycount='0'

                            if '"cited_by_tweeters_count":' in altminfo:
                                tweetstart=altminfo.find('"cited_by_tweeters_count":')+26
                                tweetend=altminfo.find(',',tweetstart)
                                tweetcount=altminfo[tweetstart:tweetend]
                            else:
                                tweetcount='0'

                            if '"details_url":"' in altminfo:
                                detailstart=altminfo.find('"details_url":"')+15
                                detailend=altminfo.find('"',detailstart)
                                detail=altminfo[detailstart:detailend]
                            else:
                                detail=''

                            
                            

                            #create issn output
                            issnout=''
                            for issn in issnlist:
                                issnout=issnout+issn+' '
                            
                            
                            

                            if validdoi=='y' and unpaywallfound=='y':

                                

                                

                                

                                if '\\' in funders:
                                    for i,j in unicodereplace:
                                        funders=funders.replace(i,j)
                                    
                                
                                outlist.append(doi);outlist.append(evidence);outlist.append(licence);outlist.append(oastatus);outlist.append(title);outlist.append(allauthors);outlist.append(authorcount);outlist.append(morethan20authors);outlist.append(wosorscopusauthors);outlist.append(numberoflocalauthors);outlist.append(localauthorlist);outlist.append(reprintauthor);outlist.append(localreprintauthor);outlist.append(localreprintauthoraddress);outlist.append(reprintauthorislocal);outlist.append(journal);outlist.append(year);outlist.append(publisher);outlist.append(isoa);outlist.append(genre);outlist.append(oajournal);outlist.append(version);outlist.append(host_type);outlist.append(greenavailable);outlist.append(repout);outlist.append(str(repositorycount));outlist.append(inlocalrepository);outlist.append(doaj);outlist.append(issnout);outlist.append(postarchiving); outlist.append(pdfarchiving);outlist.append(colour);outlist.append(cclicence);outlist.append(citations);outlist.append(freetexturl);outlist.append(inwos);outlist.append(apccharged);outlist.append(doajcurrency);outlist.append(doajprice);outlist.append(publishercurrency);outlist.append(publisherapc);outlist.append(finalapc);outlist.append(score);outlist.append(msmcount);outlist.append(policycount);outlist.append(tweetcount);outlist.append(detail);outlist.append(funders);outlist.append(crfunderlist);outlist.append(wossubject)
                            #Write the data to the .CSV file
                                
                                writer.writerow(outlist)


                                print(str(didnotexecutelist))
                                
                            else:
                                row=[doi,'DOI not found in unpaywall']
                            

                            

                            
                            print('Saving')


                            

                            #Pause to avoid overloading the APIs
                            time.sleep(2)
                            print(str(datetime.datetime.now())[11:19])

                            print()
                            

                            #Update the count
                            
                            count+=1
                            
                            
                            #Sent progress information to the screen

                            print(str(linecount)+' lines read')
                            
                            print(str(linecount)+'/'+str(recordcount)+' lines processed ('+str(int((linecount/recordcount)*100))+'%)')
                            errors=notfound+outsiderangecount
                            
                            validlines=linecount-errors
                            

                            print(str(validlines)+' valid lines')
                            

                            if count-errors>0:
                                oaperc = str(int((truecount/validlines)*100))
                                oaperc='('+oaperc+'%)'
                                print(str(truecount)+' OA documents found '+oaperc)

                            print(str(errors)+' errors')
                            print(str(notfound)+' DOIs not found')
                            
                            
                            print(str(outsiderangecount)+ ' DOIs outside year range')
                            print(str(unexecuted)+' lines did not execute')
                            
                            now=datetime.datetime.now()
                            timetaken=now-nowstart2
                            timetakenstr=str(timetaken)
                            finddot=timetakenstr.find('.')
                            
                            estimatedtime=(timetaken/count)*(recordcount-count)
                            estimatedcompletion=str(now+estimatedtime)
                            estimatedtimestr=str(estimatedtime)
                            finddot2=estimatedtimestr.find('.')
                            
                            startcomptime=estimatedcompletion.find(' ')+1
                            endcomptime=estimatedcompletion.find('.')
                            print(str(estimatedcompletion[startcomptime:endcomptime]))

                                


                            print()


                            #End of processing for the row. Program continues until the last row is completed.
                            


                        
                            if unpaywallfound=='n':
                                writer.writerow(outlist)
                                
                                print('Saving')
                                print()
                            
                                outsiderangecount+=1
                                errors+=1
                                    
                            #except:
                                #count+=1
                                #continue
                    else:
                        print('Year outside range')
                    
                        foute.write('"'+doi+'","Year outside range - '+str(year)+'"\n')
                        
                        
                        outsiderangecount+=1
                        count+=1
                        print()
                else:
                    if validdoi=='y':
                    
                        foute.write('"'+doi+'","DOI not in crossref"\n')
                    print('DOI not in crossref')
                    print()
                    errors+=1
                    notfound+=1
                done='y'
            except:
                time.sleep(10)
                retrycount+=1
                print(retrycount)
                errors+=1
                print('Line did not execute')
                
                if retrycount==8:
                    unexecuted+=1
                    foute.write('"'+doi+'","Line did not execute"\n')
                    didnotexecutelist.append(doi)
                continue
#After completion of the final row the repository data is aggregated.
#Create an output csv file

ofile=str(inf+'_'+now1+'_repositories.csv')


rel_path=newdir+"/"+ofile

abs_file_path = os.path.join(script_dir, rel_path)

of2=abs_file_path

of2=abs_file_path


#fout2=open(of2, 'w')


#Convert the repository data  list to a string
pmhliststring=str(pmhlist)

#Sort the repository list
repositorylist.sort()


#Create an output list for the aggregated repository data
replistout=[]
#Create headings
headings=['Repository','Items','Published Version','Accepted Version','Submitted Version','Null']
with open(of2, 'w', newline='',encoding='utf-8') as outputfile:
    writer = csv.writer(outputfile)
    writer.writerow(headings)


#Sent the headings to the output file



#Aggregate the data for each repository in the repository list
for repository in repositorylist:
    #Count the number of hits for the repository
    repcount=pmhliststring.count(repository)
      

    #Create a search to find all instances of  publishedVersion for that repository
    pvfind=repository+'', 'publishedVersion'
    #This gets output as a tuple so needs to be converted to a string without brackets
    pvfind=str(pvfind).replace('(','')
    pvfind=str(pvfind).replace(')','')
    publishedversioncount=pmhliststring.count(pvfind)

    avfind=repository+'', 'acceptedVersion'
    avfind=str(avfind).replace('(','')
    avfind=str(avfind).replace(')','')
    acceptedversioncount=pmhliststring.count(avfind)

    svfind=repository+'', 'submittedVersion'
    svfind=str(svfind).replace('(','')
    svfind=str(svfind).replace(')','')
    submittedversioncount=pmhliststring.count(svfind)

    nvfind=repository+'', 'null'
    nvfind=str(nvfind).replace('(','')
    nvfind=str(nvfind).replace(')','')
    nullversioncount=pmhliststring.count(nvfind)

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
    with open(of2, 'a', newline='',encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(replistout)

    #Clear the repository list ready for the next loop
    replistout=[]
#outputfile.close()

if len(funderlist)>0:

    funderlist.sort()

    statuslist=['closed','gold','diamond','bronze','green','hybrid']

    headinglist=['Funder','closed','gold','diamond','bronze','green','hybrid','Total','% Open','Closed/AAM embargoed','Closed/AAM immediate','Potential % open']
    fundercount=[]

    ofile=str(inf+'_'+now1+'_funders.csv')

    rel_path=newdir+"/"+ofile
    abs_file_path = os.path.join(script_dir, rel_path)

    

    of3=abs_file_path
    
    #funderlist=[funder.replace('\xa0',' ') for funder in funderlist]

    for i,j in unicodereplace:
        funderlist=[funder.replace(i,j) for funder in funderlist]
    
    
    
    
    with open(of3, 'w', newline='',encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(headinglist)
        outputfile.close()

        funderdata=str(funderdata)

        for i,j in unicodereplace:

            funderdata=funderdata.replace(i,j)
        
        

        for funder in funderlist:
            funderlistout=[]
            totalstatus=0
            
            

            funderlistout.append(funder)

            for status in statuslist:
                
                statuscount=funderdata.count('\''+funder+'\', \''+status)
                totalstatus=totalstatus+statuscount
                if totalstatus==0:
                    statuscount=funderdata.count('\"'+funder+'\", \''+status)
                    totalstatus=totalstatus+statuscount


                funderlistout.append(str(statuscount))
                

            

            funderlistout.append(str(totalstatus))
            
            closedcount=funderdata.count('\''+funder+'\', \'closed')
            if totalstatus>0:
                opencount=totalstatus-closedcount
                #if totalstatus<0:
                percopen=(opencount/totalstatus)*100
                percopen=str(percopen)
                finddot=percopen.find('.')
                percopen=percopen[:finddot]
            else:
                percopen='0'
            

            

            funderlistout.append(percopen)

            potentialaamembargocount=statuscount=funderdata.count('\''+funder+'\', \'closed''\', \'e')
            potentialaamcancount=statuscount=funderdata.count('\''+funder+'\', \'closed''\', \'y')

            potentialaamopen=opencount+potentialaamembargocount+potentialaamcancount

            funderlistout.append(potentialaamembargocount);funderlistout.append(potentialaamcancount)

            
            if totalstatus>0:
                perpotentialaamopen=str((potentialaamopen/totalstatus)*100)
                finddot=perpotentialaamopen.find('.')
                perpotentialaamopen=perpotentialaamopen[:finddot]
            else:
                
                perpotentialaamopen='0'

            funderlistout.append(perpotentialaamopen)

            
            
           
            
            try:
                with open(of3, 'a', newline='',encoding='utf-8') as outputfile2:
                    writer = csv.writer(outputfile2)
                    writer.writerow(funderlistout)
            except:
                print('Row did not print!')
                print(funderlistout)
                continue


   

if wosused=='Yes':
    headinglist2=['WoS Subject','closed','gold','diamond','bronze','green','hybrid','Total','% Open','Closed/AAM embargoed','Closed/AAM immediate','Potential % open']

    ofile=str(inf+'_'+now1+'_subjects.csv')

    subjectlist.sort()

    rel_path=newdir+"/"+ofile
    abs_file_path = os.path.join(script_dir, rel_path)

    of4=abs_file_path

    with open(of4, 'w', newline='',encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(headinglist2)

    



    subjectdata=str(subjectdata)
    
    

    
    for subject in subjectlist:
        
    
        subjectlistout=[]
        totalstatus=0

        subjectlistout.append(subject)
        #closedcount=0
        for status in statuslist:
            

            statuscount=subjectdata.count('\''+subject+'\', \''+status)
            
            totalstatus=totalstatus+statuscount
            if totalstatus==0:
                statuscount=subjectdata.count('\"'+subject+'\", \''+status)
                totalstatus=totalstatus+statuscount


            subjectlistout.append(str(statuscount))
            if status=='closed':
                closedcount=statuscount
            
        
        subjectlistout.append(str(totalstatus))
        closedcount=subjectdata.count('\''+subject+'\', \'closed')
        
        if totalstatus>0:
            opencount=totalstatus-closedcount
            percopen=(opencount/totalstatus)*100
            percopen=str(percopen)
            finddot=percopen.find('.')
            percopen=percopen[:finddot]
            

            
            subjectlistout.append(percopen)

                        
            potentialaamembargocount=statuscount=subjectdata.count('\''+subject+'\', \'closed''\', \'e')
            
            potentialaamcancount=statuscount=subjectdata.count('\''+subject+'\', \'closed''\', \'y')
            

            potentialaamopen=opencount+potentialaamembargocount+potentialaamcancount
            
            perpotentialaamopen=str((potentialaamopen/totalstatus)*100)
            finddot=perpotentialaamopen.find('.')
            perpotentialaamopen=perpotentialaamopen[:finddot]
            

            subjectlistout.append(potentialaamembargocount);subjectlistout.append(potentialaamcancount);subjectlistout.append(perpotentialaamopen)
            
        else:
            percopen='0'
            perpotentialaamopen='0'


        



        with open(of4, 'a', newline='',encoding='utf-8') as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow(subjectlistout)
    


if wosused=='Yes' or scopusused=='Yes':
    headinglist2=['Department','closed','gold','diamond','bronze','green','hybrid','Total','% Open','Closed/AAM embargoed','Closed/AAM immediate','Potential % open']

    ofile=str(inf+'_'+now1+'_departments.csv')

    departmentlist.sort()

    rel_path=newdir+"/"+ofile
    abs_file_path = os.path.join(script_dir, rel_path)

    of5=abs_file_path



    with open(of5, 'w', newline='',encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(headinglist2)


    departmentdata=str(departmentdata)
    
    


    #for department in departmentlist:
    for i in range(1,len(departmentlist)):
        department=departmentlist[i]
        
        departmentlistout=[]
        totalstatus=0

        departmentlistout.append(department)
        closedcount=0
        
        for status in statuslist:
            
            

            statuscount=departmentdata.count('\''+department+'\', \''+status)
            totalstatus=totalstatus+statuscount
            if totalstatus==0:
                statuscount=departmentdata.count('\"'+department+'\", \''+status)
                totalstatus=totalstatus+statuscount


            departmentlistout.append(str(statuscount))
            if status=='closed':
                closedcount=statuscount
        

        departmentlistout.append(str(totalstatus))
        #closedcount=departmentdata.count('\''+department+'\', \'closed')
        if totalstatus>0 and len(department)>0:
            opencount=totalstatus-closedcount
            percopen=(opencount/totalstatus)*100
            percopen=str(percopen)
            finddot=percopen.find('.')
            percopen=percopen[:finddot]

            
            departmentlistout.append(percopen)
            potentialaamembargocount=statuscount=departmentdata.count('\''+department+'\', \'closed''\', \'e')
            
            
            potentialaamcancount=statuscount=departmentdata.count('\''+department+'\', \'closed''\', \'y')

            potentialaamopen=opencount+potentialaamembargocount+potentialaamcancount

            perpotentialaamopen=str((potentialaamopen/totalstatus)*100)
            finddot=perpotentialaamopen.find('.')
            perpotentialaamopen=perpotentialaamopen[:finddot]

            departmentlistout.append(potentialaamembargocount);departmentlistout.append(potentialaamcancount);departmentlistout.append(perpotentialaamopen)


            
        else:
            
            percopen='0'
            perpotentialaamopen='0'
        
        try:
            
            with open(of5, 'a', newline='',encoding='utf-8') as outputfile:
                writer = csv.writer(outputfile)
                writer.writerow(departmentlistout)

        except:
            print('Row did not print!')
            print(departmentlistout)
            continue
    
#Sherpa data output. If ISSNs have been found that were not in the original input these will have been added to the output.
ofile='sherpalist.csv'
rel_path=newdir+"/"+ofile
abs_file_path = os.path.join(script_dir, rel_path)

ofsherpa=abs_file_path
sherpaheadings=['ISSN','Archive accepted manuscript','Archive published version','Sherpa/Romeo colour','Sherpa/Romeo Licence','Journal','Updated']
with open(ofsherpa, 'w', newline='',encoding='utf-8') as outputfile:  
    writer = csv.writer(outputfile)
    writer.writerow(sherpaheadings)
  
for issn in sherpadict:
    outlist=[]
    outlist.append(issn)
    sherpaentry=sherpadict.get(issn)
   


    
    for item in sherpaentry:
        outlist.append(item)
        
    
    outlist.append('')

    
    
    
    

    with open(ofsherpa, 'a', newline='',encoding='utf-8') as outputfile:  
        writer = csv.writer(outputfile)
        writer.writerow(outlist)

  
  

ofile=str(inf+'_'+now1+'_summary.txt')



rel_path=newdir+"/"+ofile
abs_file_path = os.path.join(script_dir, rel_path)

of6=abs_file_path



fout6=open(of6, 'w')
fout6.write(str(linecount)+' lines read\n')
            
fout6.write(str(count)+'/'+str(recordcount)+' lines processed ('+str(int((count/recordcount)*100))+'%)\n')



fout6.write(str(validlines)+' valid lines\n')


if count-errors>0:
    oaperc = str(int((truecount/validlines)*100))
    oaperc='('+oaperc+'%)'
    fout6.write(str(truecount)+' OA documents found '+oaperc+'\n')

fout6.write(str(errors)+' errors\n')
fout6.write(str(notfound)+' DOIs not found\n')
fout6.write(str(outsiderangecount)+ ' DOIs outside year range\n')
fout6.write(str(unexecuted)+ ' lines not executed\n')
fout6.write(str(notinsherpacount)+' additional Sherpa/Romeo records found\n')
if notinsherpacount>0:
    fout6.write('Replace the existing sherpalist.csv file in the input folder with the one generated by this iteration\n')
fout6.write('\n')
fout6.write('Input file\t')
fout6.write(infilestring+'\n')
fout6.write('Web of Science file:\t')
if wosused=='Yes':
    fout6.write(wosfilestring+'\n')
else:
    fout6.write('None\n')
fout6.write('Scopus file:\t')
if scopusused =='Yes':
    fout6.write(scopusfilestring+'\n')
else:
    fout6.write('None\n')
fout6.write('Repository address:\t')
if len(repstring)>0:
    fout6.write(repstring+'\n')
else:
    fout6.write('None\n')
if wosused=='Yes':
    fout6.write('Web of Science institutional address:\t')
    fout6.write(instita+'\n')
    if len(institb)>0:
        fout6.write('Web of Science alternative institutional address:\t')
        fout6.write(institb+'\n')
if scopusused=='Yes':
    fout6.write('Scopus institutional address\t')
    fout6.write(scopusinstnamea+'\n')
    if len(scopusinstnameb)>0:
        fout6.write('Scopus alternative institutional address\t')
        fout6.write(scopusinstnameb+'\n')
fout6.write('Year span:\t')
fout6.write(str(startyear)+'-'+str(endyear))

fout6.close()
foute.close()

print('Finished!')