# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:49:55 2019

@author: jbc28

This script helps to organize output from several FRED variable files into 
a single CSV file for analysis, plotting, etc. 

"""

import os


################### SET THESE PARAMETERS...

DirExe = '/home/chuk/FRED/models/ntp/'
DirIn = '/home/chuk/FRED/RESULTS/JOB/_JOB_ID_/OUT/PLOT/DAILY/'
DirOut = DirExe
FileOut = 'Output.csv'

# what CSV column numbers are important?
# (note: the first column is 0)
ColsToGet = [5]

# what files are important?
QuickFileList = ['',
                 'Popsize.csv',
                 'Cig.RegUse.csv',
                 'Cig.Quitfail.csv',
                 'Vape.RegUse.csv',
                 'Vape.Quitfail.csv',
                 '']

LargeFileList = ['',
                 'Popsize.csv',
                 'Vape.NoUse.csv',
                 'Vape.RegUse.csv',
                 'Vape.Quitfail.csv',
                 'Vape.Quit.csv',
                 'Cig.NoUse.csv',
                 'Cig.RegUse.csv',
                 'Cig.Quitfail.csv',
                 'Cig.Quit.csv',
                 'Cig.newQuit.csv',
                 '']

# pick a file list...
FileList = QuickFileList


################### DON'T MESS WITH THE REST...

with open(DirExe+'simulation.tmp', 'r') as SimData:
    FirstLine = SimData.readline().strip()
    JobID = str(FirstLine.split(' ')[-1])
    DirIn = DirIn.replace('_JOB_ID_',JobID)
    FileOut = FileOut.replace('.','_'+JobID+'.')




DataDict={}
def GetData(f, DirIn=DirIn,ColsToGet=ColsToGet, DataDict=DataDict):
    NameDict={}
    with open(DirIn+f, 'r') as FOpen:
        LineCount = 0
        for Line in FOpen:
            DataLine = Line.split(',')
            if LineCount == 0:
                for Col in ColsToGet:
                    Name = f[:-4]+'.'+DataLine[Col]
                    DataDict[Name]=[]
                    NameDict[Col]=Name
            else:
                for Col in ColsToGet:
                    DataDict[NameDict[Col]].append(DataLine[Col])
            LineCount += 1 
    return DataDict
    
# read files from DirIn
files = os.listdir(DirIn)
files.sort()

# match available files to the FileList and add data to DataDict
for f in files:
    if f in FileList:
        DataDict = GetData(f)

# ordered list of dictionary keys from DataDict (alphabetized)
Keys = sorted(DataDict.keys())
# number of rows in the output
ListLen = len(DataDict[Keys[0]])

# write header row as DataDict key values
with open(DirOut+FileOut, 'w') as WOut:
    WOut.write(','.join(Keys)+'\n')

# append data from associated DataDict values
with open(DirOut+FileOut, 'a') as AOut:
    DataList=[] 
    i = 0
    while i < ListLen:
        for k in Keys:
            DataList.append(DataDict[k][i])
        AOut.write(','.join(DataList)+'\n')
        i += 1
        DataList = []
