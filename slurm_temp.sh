#!/usr/bin/sh
#SBATCH --job-name=<name-of-the-job>
#SBATCH --output=<output-file-name.out>
#SBATCH --cpus-per-task=<#-of-cpus>
#SBATCH --mem=<memory-in-MB>
#SBATCH --time=<days-hr:min:sec>
#SBATCH --partition=<name-of-the-partition>

source /home/<username>/.bashrc
srun mono $<MQ-alias> <path-to-mqpar.xml>
#srun mono $MQ_1_6_14_0 /work/project/becimh_005/Shibo2/mqpar_mod_14.xml --partial-processing=16
