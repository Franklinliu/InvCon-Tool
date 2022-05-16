#!/bin/bash
cd examples/java-examples/StackAr
javac -g DataStructures/*.java
java -cp .:$DAIKONDIR/daikon.jar daikon.DynComp DataStructures.StackArTester
java -cp .:$DAIKONDIR/daikon.jar daikon.Chicory --daikon \
	--comparability-file=StackArTester.decls-DynComp \
	DataStructures.StackArTester
java -cp .:$DAIKONDIR/daikon.jar daikon.PrintInvariants StackArTester.inv.gz > StackArTester_inv.txt
