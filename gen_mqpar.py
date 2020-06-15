#!/home/waftab/anaconda3/bin/python
#coding: utf-8

import argparse
import os
import sys
import re
import time
import pdb

parser = argparse.ArgumentParser(description='MaxQuant fun')
parser.add_argument('input_xml', type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('raw_file_folders', type=str, nargs='+')
parser.add_argument('-o', '--outfile', type=str, required=True)
#parser.add_argument('-mq', '--mq-version', type=str, default='1_6_6_0', choices=['1_6_6_0'], help='MaxQuant version')
parser.add_argument('-mq', '--mq-version', type=str, default='1_6_6_0', help='MaxQuant version')
parser.add_argument('-t', '--threads', type=int, default=120, help='Number of threads to specify in MaxQuant configuration file')

args = parser.parse_args()
#pdb.set_trace()
mqpar = open(args.input_xml.name, 'r')
mqpar_text = mqpar.read()
mqpar.close()

file_counter = 0
file_path_repl_text = '<filePaths>\n'

for folder in args.raw_file_folders:
    dirs = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    # only select directories endind with d
    dirs = [d for d in dirs if d[-2:] == '.d']
    for dir in dirs:
        file_path_repl_text += ('\t<string>' + os.path.join(os.path.abspath(folder), dir) + '</string>\n')
        file_counter += 1 
        
file_path_repl_text += '   </filePaths>'

mqpar_text = re.sub(r'\<filePaths\>(.|\n|\r)*\<\/filePaths\>', file_path_repl_text, mqpar_text)

# change experiments, fractions, ptms, paramGroupIndices to reflect # of raw files added
experiments_text = '<experiments>\n'
fractions_text = '   <fractions>\n'

ptms_text = '   <ptms>\n'
group_inds_text = '   <paramGroupIndices>\n'
reference_channels_text = '   <referenceChannel>\n'

for i in range(0, file_counter):
  experiments_text += '\t<string>Exp'+f"{i+1:02d}"+'</string>\n'
  fractions_text += '\t<short>32767</short>\n'
  ptms_text += '\t<boolean>False</boolean>\n'
  group_inds_text += '\t<int>0</int>\n'
  reference_channels_text += '\t<string></string>\n'

experiments_text += '   </experiments>\n'
fractions_text += '   </fractions>\n'
ptms_text += '   </ptms>\n'
group_inds_text += '   </paramGroupIndices>\n'
reference_channels_text += '   </referenceChannel>'

mqpar_text = re.sub(r'\<experiments\>(.|\n|\r)*\<\/referenceChannel\>', \
  experiments_text+fractions_text+ptms_text+group_inds_text+reference_channels_text, mqpar_text)

# replace fasta path
fasta_path = '/work/project/becimh_005/MQ_Test/uniprot_3AUP000000803_Drosophila_melanogaster_20180723.fasta'
fasta_path = ('<fastaFilePath>' + fasta_path + '</fastaFilePath>')
mqpar_text = re.sub(r'\<fastaFilePath\>(.|\n|\r)*\<\/fastaFilePath\>', fasta_path, mqpar_text)

# replace number of threads
threads_tag = ('<numThreads>' + str(args.threads) + '</numThreads>')
mqpar_text = re.sub(r'\<numThreads\>(.|\n|\r)*\<\/numThreads\>', threads_tag, mqpar_text)

# write the MQ version
MQ_version = ('<maxQuantVersion>' + re.sub(r"_", ".", str(args.mq_version)) + '</maxQuantVersion>') 
mqpar_text = re.sub(r'\<maxQuantVersion\>(.|\n|\r)*\<\/maxQuantVersion\>', MQ_version, mqpar_text)

# write XML file
out_file = open(args.outfile, 'w')
out_file.write(mqpar_text)
out_file.close()
print('XML write success!')

### create the slurm script
slurm_script = ('#!/bin/sh\n'
'#SBATCH --job-name={JOBNAME}\n'
'#SBATCH --output={JOBNAME}.out\n'
'#SBATCH --ntasks=1\n'
'#SBATCH --cpus-per-task=16\n'
'#SBATCH --mem-per-cpu=1000\n'
'#SBATCH --time=24:0:0\n'
'#SBATCH --partition=general\n\n'
'source /home/waftab/.bashrc\n'
'srun mono ${MQ_VERSION} {MQPAR}\n'
)

# create the folder
output_folder="Slurm_Scripts"
if not os.path.exists(output_folder):
  os.makedirs(output_folder)

# replace variables in the slurm script
slurm_script = re.sub(r'{MQ_VERSION}', ('MQ_' + args.mq_version), slurm_script)
slurm_script = re.sub(r'{MQPAR}', os.path.abspath(args.outfile), slurm_script)
slurm_script = re.sub(r'{JOBNAME}', os.path.basename(output_folder), slurm_script)

# write slurm script - same format as the output folder
slurm_script_path = os.path.abspath(output_folder)+'/slurm.sh'
slurm_script_file = open(slurm_script_path, 'w')
slurm_script_file.write(slurm_script)
slurm_script_file.close()
print('Slurm script write success!')
