import csv, operator
import math
import numpy as np
import os
import sys

#~ primer parametro : la clase ejemplo FilterComparator
#~ segundo parametro: la carpeta ejemplo collections.comparators
#~ tercer parametro: el method ejemplo Randoop
archivo = (str)(sys.argv[1])
carpeta = (str)(sys.argv[2])
method = (str)(sys.argv[3])

file = open(archivo+'.csv',"w")

file.write( "Method, Class, ConverLine, ConverBranch, MutationScore, CodeLine"+ '\n')


rootDitPitest = carpeta+'.'+archivo+'/pitest'
listMutation = []		
for dirNamePitest, subdirListPitest, fileListPitest in os.walk(rootDitPitest):
	
	for fnamePit in fileListPitest:
		#~ fnamePit tengo los archivos mutations.csv	
		with open (dirNamePitest+'/'+fnamePit) as csvarchivoPit:
			entradaPit = csv.reader(csvarchivoPit)
			mutationKilled = 0.0
			mutationTotal = 0.0
			mutationScore = 0.0
			
			for regPit in entradaPit:
				mutationTotal = mutationTotal + (float)(regPit[4])
				if((str)(regPit[5]) == 'KILLED'):
					mutationKilled = mutationKilled + (float)(regPit[4]) 
				
			mutationScore = round(((float)(mutationKilled/mutationTotal)),2)
		listMutation.append(mutationScore)


rootDitCloc = carpeta+'.'+archivo+'/cloc'
listCloc = []
countLine= 0		

for dirNameCloc, subdirListCloc, fileListCloc in os.walk(rootDitCloc):
	
	for fnameCloc in fileListCloc:
		#~ fnamePit tengo los archivos cloc.csv	
		with open (dirNameCloc+'/'+fnameCloc) as csvarchivoCloc:
			entradaCloc = csv.reader(csvarchivoCloc)
			
			for regCloc in entradaCloc:
				listaCountLine = regCloc[0].split(' ')
				tam = len(listaCountLine) - 1 
				if ((str)(listaCountLine[0]) == 'Java'):
					countLine = (int)(listaCountLine[tam])
	
		listCloc.append((str)(countLine))
listCoverLine = []
listCoverBranch = []
index = 0
rootDitjacoco = carpeta+'.'+archivo+'/jacoco'	
#~ con este for completo los datos de JACOCO
for dirName, subdirList, fileList in os.walk(rootDitjacoco):	
	#~ print('Directorio encontrado: %s' %dirName)
	for fname in fileList:	
		with open (dirName+'/'+fname) as csvarchivo:
			entrada = csv.reader(csvarchivo)

			for reg in entrada:
				
				if ((str)(reg[2]) == archivo):
					coverLine = round((((float)(reg[4])/ ((float)(reg[4])+(float)(reg[3])))),2)
					coverBranch = round((((float)(reg[6])/ ((float)(reg[6])+(float)(reg[5])))),2)
					mutScore = listMutation[index]
					sizeCode = listCloc[index]
					file.write(method+', '+carpeta+'.'+archivo +', '+ (str)(coverLine)+', '+ (str)(coverBranch) +', '+ (str)(mutScore)+', '+ (str)(sizeCode)  +'\n')
					listCoverLine.append(coverLine)
					listCoverBranch.append(coverBranch)
					index = index + 1
					print(index) 

averageCoverLine=0.0
for lcL in listCoverLine:
	averageCoverLine = averageCoverLine + (float)(lcL)

averageCoverBranch=0.0
for lcB in listCoverBranch:
	averageCoverBranch = averageCoverBranch + (float)(lcB)
	
averageMutScore=0
for cM in listMutation:
	averageMutScore = averageMutScore + (float)(cM)
	
averageCountLine=0.0
for lcLine in listCloc:
	averageCountLine = averageCountLine + (float)(lcLine)
	
averageCoverLine = round(averageCoverLine/30,2)
averageCoverBranch = round(averageCoverBranch/30,2)
averageMutScore = round(averageMutScore/30,2)
averageCountLine = round(averageCountLine/30,2)
file.write('Averages, '+ carpeta+'.'+archivo +','+ (str)(averageCoverLine) +','+ (str)(averageCoverBranch) +','+ (str)(averageMutScore) +','+ (str)(averageCountLine) )						
