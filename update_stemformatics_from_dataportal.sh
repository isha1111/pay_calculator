#! /bin/bash

#cd /data/tmp

ds_id="$1"

base_url='http://127.0.0.1:5000'

CMD="wget -O - $base_url/api/update_dataset_from_data_portal?ds_id="$ds_id

eval $CMD
# execute if not running
#if [ ! -f ${lockfile}  ]
#then
#    touch  ${lockfile}
#    eval $CMD
#    rm  ${lockfile}
#fi



