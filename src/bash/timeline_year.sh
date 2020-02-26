#!/bin/bash
# arguments:
# $1: month of IPhO to be created
# $2: previous month if exists, 0 otherwise
# $3: next month if exists, 0 otherwise
# $4: number of IPhO to be created
echo "Creating timeline/$1"
mkdir -p ../timeline/$1
source timeline_month_index.sh $1 $2 $3
source timeline_month_country.sh $1 $2 $3 $4
source timeline_month_individual.sh $1 $2 $3 $4