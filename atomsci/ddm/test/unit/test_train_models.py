   #!/usr/bin/env python

import json
import numpy as np
import pandas as pd
import os
import sys
import tarfile
import tempfile
import logging
from datetime import timedelta
from datetime import datetime
import argparse
import atomsci.ddm.pipeline.model_pipeline as mp
import atomsci.ddm.pipeline.parameter_parser as parse

import time
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
running_in_virtualenv = "VIRTUAL_ENV" in os.environ

def train_model(input, output):
    train_json_f = input
    #train_json_f = '/g/g20/mauvais2/workspace/tmp/AMPL/atomsci/ddm/data/parp1_gcn_params.json'
    #train_json_f = '/g/g20/mauvais2/workspace/tmp/AMPL/atomsci/ddm/data/parp1_graphconv_params.json'
    #out_dir = '/p/lustre1/mauvais2/model_retrain'
    # /usr/WS2/atom/PARP_compounds/Datasets_and_Models/PARP1/parp1_gcn_params.json
    # /usr/WS2/atom/PARP_compounds/Datasets_and_Models/PARP1/parp1_graphconv_params.json
    # maybe the model_type is supposed to be 'GCNModel'
    # change save_results to False in the parameter files so your models get saved locally.

    start_time = time.time()
    with open(train_json_f) as f:
        config = json.loads(f.read())

    # Parse parameters
    params = parse.wrapper(config)
   # if not (output and output.strip()):
   #     params.result_dir = output

    print('output dir: ' +  params.result_dir, flush=True)
    # Create model pipeline
    model = mp.ModelPipeline(params)
    # Train model
    model.train_model()

    # print env info
    running_in_virtualenv = bool(os.getenv("VIRTUAL_ENV"))
    print('============', flush=True)
    print('Input Json: '  + train_json_f, flush=True);
    print('Running host: ' +  os.uname()[1], flush=True);

    if running_in_virtualenv:
        print('Running VM: ' + os.environ['VIRTUAL_ENV'], flush=True)
    elapsed_time_secs = time.time() - start_time
    print("Start time: %s " % datetime.fromtimestamp(float(start_time)).strftime("%Y-%m-%d %H:%M:%S"), flush=True)
    print("Execution took: %s " % timedelta(seconds=round(elapsed_time_secs)), flush=True)

#----------------
# main
#----------------
def main(argv):

    # input file/dir (required)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='input model file')
    parser.add_argument('-o', '--output', default='', help='output directory')

    args = parser.parse_args()

    for x in range(4):
        print('========***===========', flush=True)
        print('Start '  + str(x) + ' training iteration:', flush=True)
        train_model(args.input, args.output)
        time.sleep(10)

if __name__ == "__main__":
   main(sys.argv[1:])


