#!/usr/bin/sh
#SBATCH --job-name=MQ_fat
#SBATCH --output=MQ_fat.out
#SBATCH --cpus-per-task=32
#SBATCH --mem=256000
#SBATCH --time=30-00:00:00
#SBATCH --partition=fat

source /home/waftab/.bashrc
srun mono $MQ_1_6_14_0 /work/project/becimh_005/Shibo2/mqpar_mod_14.xml
#srun mono $MQ_1_6_14_0 /work/project/becimh_005/Shibo2/mqpar_mod_14.xml --partial-processing=16
