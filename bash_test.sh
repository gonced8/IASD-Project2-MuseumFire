#!/bin/bash

for algorithm in 0 1; do
    for file_name in public_tests/*; do
	if [ "${algorithm}" = "0" ]  
	then
	    gtimeout -v 120 gtime -f %e python3 main.py "${file_name}" 0 "${algorithm}" >> ficheiro1_time.txt 2>&1
            gtimeout -v 120 gtime -f %M python3 main.py "${file_name}" 0 "${algorithm}" >> ficheiro1_memory.txt 2>&1
	fi
	if [ "${algorithm}" = "1" ]  
	then
	    gtimeout -v 120 gtime -f %e python3 main.py "${file_name}" 0 "${algorithm}" >> ficheiro2_time.txt 2>&1
            gtimeout -v 120 gtime -f %M python3 main.py "${file_name}" 0 "${algorithm}" >> ficheiro2_memory.txt 2>&1
	fi
    done
done
