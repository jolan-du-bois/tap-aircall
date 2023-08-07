#!/bin/sh

# mode="$1"
# timestamp=$(date +%s)

# poetry install

# if [ "$mode" = "catalog" ]
# then
#   echo "Mode $mode: running without state"
#   poetry run tap-aircall \
#     --config .secrets/config.json >> output/output_${timestamp}.json
#   tail -1 output/output_${timestamp}.json >> samples/state.json.tmp && mv samples/state.json.tmp samples/state.json
#   cat output/output_${timestamp}.json | grep RECORD >> output/output_record_${timestamp}.json
# elif [ "$mode" = "state" ]
# then
#   echo "Mode $mode: running with state config from sample"
#   poetry run tap-aircall \
#   --config .secrets/config.json \
#   --state samples/state.json >> output/output_${timestamp}.json
#   cat output/output_${timestamp}.json | grep RECORD >> output/output_record_${timestamp}.json
# else
#     echo "Mode $mode: running nothing"
# fi

mode="$1"
timestamp=$(date +%s)

if [ "$mode" = "catalog" ]
then
  poetry install
  echo "Mode $mode: running without state"
  poetry run tap-aircall \
    --config .secrets/config.json >> output/output_${timestamp}.json
  tail -1 output/output_${timestamp}.json >> samples/state.json.tmp && mv samples/state.json.tmp samples/state.json
  python samples/create_sample.py 
  cat output/output_${timestamp}.json | grep RECORD >> output/output_record_${timestamp}.json
elif [ "$mode" = "state" ]
then
  poetry install
  echo "Mode $mode: running with state config from sample"
  poetry run tap-aircall \
  --config .secrets/config.json \
  --state samples/state.json >> output/output_${timestamp}.json
  cat output/output_${timestamp}.json | grep RECORD >> output/output_record_${timestamp}.json
elif [ "$mode" = "--about" ]
then 
  echo "Options and arguments :"
  echo "  catalog : retrieves all data starting from the date specified in .secrets/config.json"
  echo "  state : retrieves all data starting from the state indicated in samples/state.json"
else
  echo "Mode $mode: running nothing"
fi