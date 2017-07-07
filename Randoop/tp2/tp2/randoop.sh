#!/bin/bash

#~ se le pasan dos parametros
#~ ./randoop.sh collections.comparators FixedOrderComparator

cp src/allTestSuiteRandoop/$2/pom.xml pom.xml

mvn clean install

for m in $(seq 20 1 30)
	do 
		echo $m		
		mkdir src/allTestSuiteRandoop/$2/test$m
		mkdir src/dataRandoop/$1.$2/jacoco/medidas.jacoco.$1.$2.$m
		mkdir src/dataRandoop/$1.$2/pitest/medidas.pitest.$1.$2.$m
		java -ea -classpath ../randoop-all-3.1.5.jar:target/classes randoop.main.Main gentests --classlist=$2.txt --timelimit=60 --testsperfile=500 --junit-output-dir=src/test/java --randomseed=$m
		rm src/test/java/Error*.java
		mvn test
		cp src/test/java/* src/allTestSuiteRandoop/$2/test$m
		cp target/site/jacoco/jacoco.csv src/dataRandoop/$1.$2/jacoco/medidas.jacoco.$1.$2.$m
		
		mvn clean install org.pitest:pitest-maven:mutationCoverage -DoutputFormats=CSV
		cp target/pit-reports/*/* src/dataRandoop/$1.$2/pitest/medidas.pitest.$1.$2.$m
		rm src/test/java/*.java
	done		

rm pom.xml
