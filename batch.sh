#!/usr/bin/env bash

vanilla=vanilla
selective=selective
device=0
root_dir=/data/meijiajie/data_processing

for data in LCSTS UGC
do
    for merge in 30000 35000 40000
    do
        cd ${root_dir}/${data}/subworded_${merge}/
        git clone https://github.com/Jiajie-Mei/pointer-generator.git
        cd pointer-generator && git checkout master && cp -r ../finished_files . && cd ..
        cp -r pointer-generator ${vanilla} && cd ${vanilla}
        nohup bash run.sh ${device} 4 ${data} nonselective &
        cd ..
        cp -r pointer-generator ${selective} && cd ${selective}
        nohup bash run.sh ${device} 4 ${data} selective &
        cd ..
        rm -rf pointer-generator
    done
    let device=${device}+1
    let device=${device}%2
done
