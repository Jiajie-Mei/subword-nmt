#!/usr/bin/env bash

vanilla=vanilla
selective=selective
train=2
eval1=3
eval2=4

root_dir=/data/meijiajie/data_processing
pure_test=pure_test.sh

for data in LCSTS UGC
do
    for merge in 30000 40000
    do

        cd ${root_dir}/${data}/subworded_${merge}/${vanilla}
        if [ "$(pwd)" = "/data/meijiajie/data_processing/LCSTS/subworded_40000/vanilla" ]
        then
        echo skip $(pwd)
        else
            head -31 run.sh > ${pure_test} && tail -14 run.sh >> ${pure_test}
            rm -rf log/mei/dec
            nohup bash ${pure_test} ${train} ${eval1} ${data} nonselective &
        fi
        cd ../${selective}
        nohup bash ${pure_test} ${train} ${eval1} ${data} selective &

        let train=${train}%3+2
        let temp=${eval1} && let eval1=${eval2} && let eval2=${temp}
    done
done
