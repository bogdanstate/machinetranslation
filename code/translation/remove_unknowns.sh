awk -F'\t' '{if ($3="<unknown>") $3=$1; print $1"\t"$2"\t"$3}'
