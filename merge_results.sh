#!/bin/bash

for file_name in public_tests/*; do
    name=${file_name##*/}
    echo "${name}" >> file_direct.txt 2>&1
done

rm -v testefileaux
:|paste -d' ;' file_direct.txt - ficheiro1_time.txt - ficheiro2_time.txt - ficheiro1_memory.txt - ficheiro2_memory.txt > testefileaux.txt

rm -v file_direct.txt
