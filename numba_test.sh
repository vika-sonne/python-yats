 #!/usr/bin/env bash

CSV_FILE=images/numba_tests.csv

echo "-----------"
echo "Numba tests"
echo "-----------"

echo "Clean up directory..."
rm -v ./$CSV_FILE
echo "done"

echo "Generate binary by numba..."
numba numba_gen.py
echo "done"

echo "Run numba tests..."
python3 numba_run.py > $CSV_FILE
echo "done"

echo "Run python tests..."
pypy3 numba_run.py >> $CSV_FILE
echo "done"

echo "Convert test results to graphs: .csv files to .png..."
python3 csv_to_png.py -v ./$CSV_FILE
echo "done"
