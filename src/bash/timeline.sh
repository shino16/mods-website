#!/bin/bash
echo "Creating timeline"
mkdir -p ../timeline
source timeline_index.sh
# TODO
source timeline_month.sh 2012 2011 2013 43
source timeline_month.sh 2013 2012 2014 44