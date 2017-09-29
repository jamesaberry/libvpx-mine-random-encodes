#!/usr/bin/python

import sys, random
from os import path
from os import system
from os.path import basename
from datetime import datetime
import subprocess

def output_settings(output_file_str, commandline):
    
    text_file = open(output_file_str + ".settiings", "w")
    text_file.write(commandline)
    text_file.close()

def generate_output_file_name(input_file_str):
    dt = datetime.now()
    return input_file_str + "_" + dt.strftime('%Y_%m_%d_%H_%M_%S') + ".webm"

# select random parameters using dictionary and range
def select_params(params):
    
    param_str = ""
    for key in params:
        random.seed()
        param_str += key + str(random.randint(params[key][0], params[key][1])) + " "
        
    return param_str

# select qualifiers given quantizer conditions.
def select_quantifers(qparams):
    
    quant_sel = dict()
    quant_sel_state = False
    
    while not quant_sel_state:
        for key in qparams:
            quatizer = random.randint(qparams[key][0], qparams[key][1])
            quant_sel[key] = quatizer

        diff =  list(quant_sel.values())[1] -list(quant_sel.values())[0]
        
        # max must be gt min, must be 8 apart, must not be the same
        if  diff > 8 and diff != 0:
            quant_sel_state = True
        
    quant_str = ""
    for key in quant_sel:
        quant_str += key + str(quant_sel[key]) + " "
            
    return quant_str

def run_random_encode():
    
    pathstr = path.abspath(sys.modules['__main__'].__file__)
    
    # must not be = and must be at least 8 apart
    qparams = {"--min-q=" : [0,63], 
               "--max-q=" : [0,63]} 

    #"--usage=" :  []
    #"--kf-min-dist=" : [0,60], not supported in auto
    params = { "--passes=" : [1,2],
               "--error-resilient=" : [0,1],
               "--lag-in-frames=" : [0,20],
               "--drop-frame=" : [0,100],
               "--resize-allowed=" : [0,1],
               "--target-bitrate=" : [200 , 50000],
               "--undershoot-pct=" : [0,100],
               "--overshoot-pct=" : [0,100],
               "--buf-sz=" : [0, 500],
               "--buf-initial-sz=" : [0,500],
               "--buf-optimal-sz=" : [0,500],
               "--kf-max-dist=" : [0,60],
               "--cpu-used=" : [-8,8],
               "--auto-alt-ref=" : [0,1],
               "--sharpness=" : [0,7],
               "--arnr-maxframes=" : [0,15],
               "--arnr-strength=" : [0,6],
               "--gf-cbr-boost=" : [0,100],
               "--lossless=" : [0,1],
               "--frame-parallel=" : [0,1],
               "--aq-mode=" : [0,4],
               "--frame-boost=" : [0,1],
               "--row-mt=" : [0,1]
               }

    # add more files here eventually
    input_files = ["720p50_parkrun_ter.y4m"]

    ################# Assemble random command line #################
    end_use_str = "--end-usage=" + ["vbr", "cbr", "cq", "q"][random.randint(0, 3)]
    profile_str = "--profile=" + str(random.choice([0]))
    input_file_str = random.choice(input_files)
    output_file_str = generate_output_file_name(input_file_str)
    
    commandline = "--verbose --psnr " + select_quantifers(qparams) \
        + select_params(params) + profile_str + " " + end_use_str  \
        + " --output=" + output_file_str + " " + input_file_str
    
    output_settings(output_file_str, commandline)
    
    run_cmd = pathstr.rsplit('\\',1)[0] + "\\vpxenc.exe " + commandline
    
    with open(output_file_str + ".log", 'w') as output_f:
        subprocess.Popen(run_cmd, stdout=output_f, stderr=output_f)

    system(run_cmd)
    
def main(argv):
    
    while True:
        run_random_encode()

if __name__ == "__main__":
   main(sys.argv[1:])
