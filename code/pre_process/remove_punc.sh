cat $1 | tr -ds '[:punct:][:digit:]' '' | tr '[:upper:]' '[:lower:]' > $2