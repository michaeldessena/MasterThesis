#!/usr/bin/bash


eval `scram runtime -sh`
i=0

list=$(find ${1} -name "00*" -type d)

array=()
while IFS=  read -r -d $'\0'; do
    array+=("$REPLY")
done < <(find ${1} -name "00*" -type d -print0)

for file in $list; do
    result=${file}/result.yoda
    if [ -f "${result}" ]; then
        echo "${result} exist"
        i=$((i+1))
    else
        rm -r ${file}
        echo "${result} doesn t exist --- /// --- ${file} REMOVED!!!"
    fi
done
i=$((i-1))
k=1

for (( j=0; j<=$i; j=j+1 )); do
    result=${1}/$(printf "%04d" ${j})
    if  [ -d "${result}" ]; then
        echo "${result} exist!!!"
    else
        lenght=$((${#array[*]}-$k))
        mv ${array[$lenght]} ${result}
        echo "${array[$lenght]} -----> $result"
        k=$((k+1))
    fi
done
echo "${#array[*]}"