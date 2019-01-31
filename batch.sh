#!/usr/bin/env bash

vanilla=vanilla
selective=selective
train=0
eval1=3
eval2=4

root_dir=/data/meijiajie/data_processing

cd ${root_dir}
git clone https://github.com/Jiajie-Mei/pointer-generator.git
cd pointer-generator && git checkout master

for data in LCSTS UGC
do
    for merge in 30000 35000 40000
    do

        cd ${root_dir}/${data}/subworded_${merge}/
        cp -r ${root_dir}/pointer-generator .
        cd pointer-generator && cp -r ../finished_files . && cd ..
        cp -r pointer-generator ${vanilla} && cd ${vanilla}
        nohup bash run.sh ${train} ${eval1} ${data} nonselective &
        cd ..
        cp -r pointer-generator ${selective} && cd ${selective}
        nohup bash run.sh ${train} ${eval1} ${data} selective &
        cd ..
        rm -rf pointer-generator
        let train=${train}+1
        let train=${train}%3
        let temp=${eval1} && let eval1=${eval2} && let eval2=${temp}
    done
done

cd ${root_dir} && rm -rf pointer-generator
