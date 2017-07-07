#!/bin/bash


cp src/allTestSuiteEvoSuite/$2/pom.xml pom.xml
mvn clean install

#~ primer parametro es: collections.
#~ segundo parametro es: comparators
#~ tercer parametro es: la clase a testear (FixedOrderComparator)

for m in $(seq 1 1 30)

	do 
		echo $m
		mkdir src/allTestSuiteEvoSuite/$3/test$m
		mkdir src/dataEvoSuite/medidas.jacoco.$1.$2.$3.$m	
		mkdir src/dataEvoSuite/medidas.pitest.$1.$2.$3.$m
		mkdir src/dataEvoSuite/medidas.evodatos.$1.$2.$3.$m
		java -jar evosuite-1.0.5.jar -class $1.$2.$3 -projectCP target/classes -Dsearch_budget=60 -Duse_separate_classloader=false	
		
		#~ luego tenemos en  evosuite-tests los tests generados por evosuite-tests
		
		cp evosuite-tests/$1/$2/* src/allTestSuiteEvoSuite/$3/test$m
		cp evosuite-tests/$1/$2/* src/test/java/
		#~ ahora tengo los test de evo en mi conjunto de test y en la carpera test/java
		#~ listo para ejecutar maven otra vez
		rm src/test/java/*Error*.java
		mvn test
		cp target/site/jacoco/jacoco.csv src/dataEvoSuite/medidas.jacoco.$1.$2.$3.$m
		cp evosuite-report/* src/dataEvoSuite/medidas.evodatos.$1.$2.$3.$m
		mvn clean install org.pitest:pitest-maven:mutationCoverage
		rm src/test/java/*.java
		rm evosuite-tests/*
		cp target/pit-reports/*/* src/dataEvoSuite/medidas.pitest.$1.$2.$3.$m
	done 
rm pom.xml
