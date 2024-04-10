#!/bin/bash
#by Gabriel Libânio Silva Rodrigues

# Script to run Orca quantum chemistry program, moving the temporary files to a scratch directory

# PATH to orca
ORCAPATH=${ORCAPATH}
ORCASCR=${ORCASCR}

if [ -z "${ORCAPATH}" ] || [ -z "${ORCASCR}" ]; then
	echo "To use orca-run you need to first export ORCAPATH and ORCASCR variables in your enviroment."
	exit 0
fi

# Calculation directory
CALCDIR="${PWD}"
# Variables
DATE=`date "+%d-%m-%Y"`
TIME=`date "+%H:%M:%S"`
input=""
output=""
nprocs=""
afile=""
maxcore=""
usage="SCRIPT USAGE:

orca_run -i input.inp -o output.out -p nprocs -m maxcore -a \"file1.gbw file2.xyz\" -e email@addres.com hostsender

Only input is obligatory, default output = input-basename.out
For multiple auxiliary files, use the -a option separating the file names with space and INSIDE double quotes:

-a \"file1.gbw file2.xyz\""

# Input options, passing arguments
while getopts i:o:p:a:e:m:h option
do
	case "${option}" in
		i)	input=${OPTARG}
			# New input to be placed in the runfiles folder to see modifications
			inputNEW="${input%.*}.new.inp"
			RUNDIR="${ORCASCR}/${input%.*}-$$"
			;;
		o)	output=${OPTARG};;
		p)	nprocs=${OPTARG};;
		a)	afile=${OPTARG};;
		m)	maxcore=${OPTARG};;
		h | *) # Display help.
			echo "${usage}"
			exit 0
		;;
	esac
done
shift $((OPTIND-1))

### START and show what will be done ###
echo "Orca will run on node $HOSTNAME in $DATE at $TIME with the following options" > ${input%.*}.nodes
echo "input = $input" >> ${input%.*}.nodes
echo "output = $output" >> ${input%.*}.nodes
echo "number of processors = $nprocs" >> ${input%.*}.nodes
echo "maxcore memory = $maxcore" >> ${input%.*}.nodes
echo "extrafile = $afile" >> ${input%.*}.nodes
echo "scratch directory = $RUNDIR" >> ${input%.*}.nodes

#### Starting job script ####
mkdir -p "${RUNDIR}"
cd "${RUNDIR}"
cp "${CALCDIR}/$input" "${RUNDIR}" # Copy input to run dir

### Argument Cases ###

# Case there is extra files to copy
if [ -n "$afile" ]; then
	for file in ${afile[@]}
		do cp "${CALCDIR}"/${file} "${RUNDIR}"
	done
fi
# Case no output is specified, output will be same input name with .out extension
if [ -z "$output" ]; then
	output=${input%.*}.out
fi
# Case nprocs was specified
if [ -n "$nprocs" ]; then
	## Erase possible %pal configuration in input
	sed -i -e "/^%pal.*$/Id" $input
	## Write the number of processors to inp file with requested %pal configuration
	echo "%Pal nprocs $nprocs end" | cat - $input > inputOR.temp && mv inputOR.temp $input
fi
if [ -n "$maxcore" ]; then
# Case maxcore was specified
	## Erase possible %maxcore configuration in input
	sed -i -e "/^%maxcore.*$/Id" $input
	## Write the number of processors to inp file with requested %maxcore configuration
	echo "%maxcore $maxcore" | cat - $input > inputOR.temp && mv inputOR.temp $input
fi

### Run the program itself and alert the user ####
echo "
If you need help try the option: orca_run.sh -h

Run directory = ${RUNDIR}
Orca will run with command:

${ORCAPATH}/orca ${input} > ${CALCDIR}/${output}
"

#### RUN ORCA ####
${ORCAPATH}/orca "${input}" > "${CALCDIR}/${output}"

# Do final operation on post-calculation ORCA files
mkdir -p "${CALCDIR}/${input%.*}-runfiles"
mv ${input} ${inputNEW}

for file in *; do
    if [[ $file == *.tmp* ]]; then
        rm $file
        continue
    else
        mv "$file" "${CALCDIR}/${input%.*}-runfiles"
    fi
done