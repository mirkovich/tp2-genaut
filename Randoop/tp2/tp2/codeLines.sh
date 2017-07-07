#!/bin/bash

#~ primer parametro la clase
#~ segundo parametro la ruta
for m in $(seq 1 1 30)
	do 
		cloc src/allTestSuiteRandoop/$1/test$m/ --out=cloc.csv

#~ se va a crear un archivo "out" en el mismo lugar donde se encuentra el codeLines.sh
		mkdir src/dataRandoop/$2.$1/cloc/medidas.cloc.$2.$1.$m
		cp cloc.csv src/dataRandoop/$2.$1/cloc/medidas.cloc.$2.$1.$m
		rm cloc.csv
	done
