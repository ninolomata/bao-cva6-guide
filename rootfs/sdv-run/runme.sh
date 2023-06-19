REPETITIONS=1000

cd /sdv-run/benchmarks/disparity/data

# echo disparity-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh

echo disparity-qcif
cd ./qcif
perf stat --table -n -r $REPETITIONS ./runme.sh

echo disparity-sqcif
cd ../sqcif
perf stat --table -n -r $REPETITIONS ./runme.sh

cd /sdv-run/benchmarks/localization/data

# echo localization-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh

echo localization-qcif
cd ./qcif
perf stat --table -n -r $REPETITIONS ./runme.sh

echo localization-sqcif
cd ../sqcif
perf stat --table -n -r $REPETITIONS ./runme.sh

cd /sdv-run/benchmarks/mser/data

# echo mser-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh

echo mser-qcif
cd ./qcif
perf stat --table -n -r $REPETITIONS ./runme.sh

echo mser-sqcif
cd ../sqcif
perf stat --table -n -r $REPETITIONS ./runme.sh

# cd /sdv-run/benchmarks/multi_ncut/data
# 
# echo multi_ncut-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh
# 
# echo multi_ncut-qcif
# cd ../qcif
# perf stat --table -n -r $REPETITIONS ./runme.sh
# 
# echo multi_ncut-sqcif
# cd ../sqcif
# perf stat --table -n -r $REPETITIONS ./runme.sh

cd /sdv-run/benchmarks/sift/data

# echo sift-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh

echo sift-qcif
cd ./qcif
perf stat --table -n -r $REPETITIONS ./runme.sh

echo sift-sqcif
cd ../sqcif
perf stat --table -n -r $REPETITIONS ./runme.sh

cd /sdv-run/benchmarks/stitch/data

# echo stitch-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh

echo stitch-qcif
cd ./qcif
perf stat --table -n -r $REPETITIONS ./runme.sh

echo stitch-sqcif
cd ../sqcif
perf stat --table -n -r $REPETITIONS ./runme.sh

# cd /sdv-run/benchmarks/svm/data
# 
# echo svm-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh
# 
# echo svm-qcif
# cd ../qcif
# perf stat --table -n -r $REPETITIONS ./runme.sh
# 
# echo svm-sqcif
# cd ../sqcif
# perf stat --table -n -r $REPETITIONS ./runme.sh

# cd /sdv-run/benchmarks/texture_synthesis/data
# 
# echo texture_synthesis-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh
# 
# echo texture_synthesis-qcif
# cd ../qcif
# perf stat --table -n -r $REPETITIONS ./runme.sh
# 
# echo texture_synthesis-sqcif
# cd ../sqcif
# perf stat --table -n -r $REPETITIONS ./runme.sh

cd /sdv-run/benchmarks/tracking/data

# echo tracking-cif
# cd ./cif
# perf stat --table -n -r $REPETITIONS ./runme.sh

echo tracking-qcif
cd ./qcif
perf stat --table -n -r $REPETITIONS ./runme.sh

echo tracking-sqcif
cd ../sqcif
perf stat --table -n -r $REPETITIONS ./runme.sh

cd /