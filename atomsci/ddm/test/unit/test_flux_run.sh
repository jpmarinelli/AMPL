#!/bin/sh

date
flux run -n4 python test_train_models.py -i /usr/WS2/atom/PARP_compounds/Datasets_and_Models/PARP1/parp1_gcn_params.json
echo 'job complete'
date
