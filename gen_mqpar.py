#!/home/waftab/anaconda3/bin/python
#coding: utf-8

import argparse
import os
import sys 
import re
import time

parser = argparse.ArgumentParser(description='Modify MaxQuant parameter file')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('--input_xml', '-in', type=argparse.FileType('r', encoding='UTF-8'), required=True, help='input xml file')
requiredNamed.add_argument('--raw_files_folder', '-raw', type=str, nargs='+', required=True, help='raw file\'s folder')
requiredNamed.add_argument('--fasta_file_fullpath', '-fasta', type=str, required=True, help='fasta file with full path')
requiredNamed.add_argument('--output_xml', '-out', type=str, required=True, help='output xml file')
##requiredNamed.add_argument('-mq', '--mq-version', type=str, default='1_6_6_0', choices=['1_6_6_0'], required=True, help='MaxQuant version')
requiredNamed.add_argument('--mq_version', '-mq', type=str, default='1_6_6_0', required=True, help='MaxQuant version')
requiredNamed.add_argument('--threads', '-t', type=int, default=120, required=True, help='Number of threads')
args = parser.parse_args()

## read input xml
mqpar = open(args.input_xml.name, 'r')
mqpar_text = mqpar.read()
mqpar.close()
#print(mqpar)
#print(mqpar_text)

## replace fasta file's path in the xml
#fasta_file_fullpath = ('<fastaFilePath>' + re.sub(r"_", ".", str(args.fasta_file_fullpath)) + '</fastaFilePath>')
fasta_file_fullpath = ('<fastaFilePath>' +  str(args.fasta_file_fullpath) + '</fastaFilePath>')
mqpar_text = re.sub(r'\<fastaFilePath\>(.|\n|\r)*\<\/fastaFilePath\>', fasta_file_fullpath, mqpar_text)
#print(fasta_file_fullpath)

## replace the raw files path in the xml
file_counter = 0 
file_path_repl_text = '<filePaths>\n'

for folder in args.raw_files_folder:
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

# replace number of threads
threads_tag = ('<numThreads>' + str(args.threads) + '</numThreads>')
mqpar_text = re.sub(r'\<numThreads\>(.|\n|\r)*\<\/numThreads\>', threads_tag, mqpar_text)

# write the MQ version
MQ_version = ('<maxQuantVersion>' + re.sub(r"_", ".", str(args.mq_version)) + '</maxQuantVersion>')
mqpar_text = re.sub(r'\<maxQuantVersion\>(.|\n|\r)*\<\/maxQuantVersion\>', MQ_version, mqpar_text)

## write output xml file
out_file = open(args.output_xml, 'w')
out_file.write(mqpar_text)
out_file.close()
print('XML write success!')

#!/usr/bin/sh
#SBATCH --job-name=MQ
#SBATCH --output=MQ.out
#SBATCH --cpus-per-task=72
#SBATCH --mem=256000
#SBATCH --time=30-00:00:00
#SBATCH --partition=slim18

#source /home/waftab/.bashrc
#srun mono $MQ_1_6_14_0 /work/project/becimh_005/Shibo3/mqpar_mod_14.xml
#srun mono $MQ_1_6_15_0 /work/project/becimh_005/Shibo3/mqpar_mod_15.xml
## create the slurm script
slurm_script = ('#!/usr/bin/sh\n'
'#SBATCH --job-name={JOBNAME}\n'
'#SBATCH --output={JOBNAME}.out\n'
'#SBATCH --cpus-per-task=72\n'
'#SBATCH --mem-per-cpu=256000\n'
'#SBATCH --time=00-24:00:00\n'
'#SBATCH --partition=slim18\n\n'
'source /home/waftab/.bashrc\n'
'srun mono ${MQ_VERSION} {MQPAR}\n'
)

## create the folder
output_folder="Slurm_Scripts"
if not os.path.exists(output_folder):
  os.makedirs(output_folder)

# replace variables in the slurm script
slurm_script = re.sub(r'{MQ_VERSION}', ('MQ_' + args.mq_version), slurm_script)
slurm_script = re.sub(r'{MQPAR}', os.path.abspath(args.output_xml), slurm_script)
slurm_script = re.sub(r'{JOBNAME}', os.path.basename(output_folder), slurm_script)

# write slurm script - same format as the output folder
slurm_script_path = os.path.abspath(output_folder)+'/slurm.sh'
slurm_script_file = open(slurm_script_path, 'w')
slurm_script_file.write(slurm_script)
slurm_script_file.close()
print('Slurm script write success!')
