 #!/usr/bin/env bash

TEST_GROUPS=3
CSV_FILE_PREF=images/speed_tests_

run_tests() {
	IMPLEMENTATION=$1
	echo "	Run tests for ${IMPLEMENTATION}..."
	for i in `seq $TEST_GROUPS`; do
		if [ ! -f ./${CSV_FILE_PREF}${i}.csv ]; then $IMPLEMENTATION speed_tests.py --header > ./${CSV_FILE_PREF}${i}.csv; fi
	done
	echo "		containers..."
	$IMPLEMENTATION speed_tests.py --csv -g array list memoryview bytearray tuple dict class >> ./${CSV_FILE_PREF}1.csv
	echo "		assingment variables..."
	$IMPLEMENTATION speed_tests.py --csv -g assingment variables >> ./${CSV_FILE_PREF}2.csv
	echo "		string manipulations..."
	$IMPLEMENTATION speed_tests.py --csv -g string >> ./${CSV_FILE_PREF}3.csv
	echo "	done"
}

echo "-----------"
echo "Speed tests"
echo "-----------"

echo "Clean up directory..."
for i in `seq $TEST_GROUPS`; do rm -v ./${CSV_FILE_PREF}${i}.csv; done
echo "done"

echo "Run python tests..."
run_tests python3
echo "done"

echo "Run pypy tests..."
run_tests pypy3
echo "done"

echo "Convert test results to graphs: .csv files to .png..."
for i in `seq $TEST_GROUPS`; do python3 csv_to_png.py -v ./${CSV_FILE_PREF}${i}.csv; done
echo "done"
