REPETITIONS=1000

cd /mibench/automotive/qsort
echo qsort-small
perf stat --table -n -r $REPETITIONS ./runme_small.sh

i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_small.sh
done
echo qsort-large
perf stat --table -n -r $REPETITIONS ./runme_large.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_large.sh
done

cd /mibench/automotive/susan
echo susanc-small
perf stat --table -n -r $REPETITIONS ./runme_small-c.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_small-c.sh
done
echo susanc-large
perf stat --table -n -r $REPETITIONS ./runme_large-c.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_large-c.sh
done
echo susane-small
perf stat --table -n -r $REPETITIONS ./runme_small-e.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_small-e.sh
done
echo susane-large
perf stat --table -n -r $REPETITIONS ./runme_large-e.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_large-e.sh
done
echo susans-small
perf stat --table -n -r $REPETITIONS ./runme_small-s.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_small-s.sh
done
echo susans-large
perf stat --table -n -r $REPETITIONS ./runme_large-s.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_large-s.sh
done

cd /mibench/automotive/bitcount
echo bitcount-small
perf stat --table -n -r $REPETITIONS ./runme_small.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_small.sh
done
echo bitcount-large
perf stat --table -n -r $REPETITIONS ./runme_large.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_large.sh
done

cd /mibench/automotive/basicmath
echo basicmath-small
perf stat --table -n -r $REPETITIONS ./runme_small.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_small.sh
done
echo basicmath-large
perf stat --table -n -r $REPETITIONS ./runme_large.sh
i=0
while [ $i -ne $REPETITIONS ]; do
    i=$(($i+1))
    perf stat -er1,r2,r3,r4,r5,r6,r7 ./runme_large.sh
done

cd /