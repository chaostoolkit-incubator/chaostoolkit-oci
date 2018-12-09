# This script will show the probe functions and action functions that
# the driver currently provides.
#!/usr/bin/env bash

E=$(which egrep)
S=$(which sed)
L=$(which ls)
C=$(which cut)
T=$(which tr)


CHAOSDIR=$(${L} chaos* -d --color=never|${E} -v '.log')
SEARCH_PATTERN='activities\.extend'

ACTIVITIES=$(${E} "${SEARCH_PATTERN}" "${CHAOSDIR}/__init__.py")

echo
echo "LIST OF ACTIVITIES WITHIN ${CHAOSDIR}"
echo

for line in ${ACTIVITIES[@]}; do
	SERV_TYPE=$(echo ${line}|${S} "s/^.*(\"//;s/\").*$//;s/${CHAOSDIR}\.//")

	# Split the pathname
	SERVICE=$(echo ${SERV_TYPE}|${C} -d. -f1)
	TYPE=$(echo ${SERV_TYPE}|${C} -d. -f2)

	echo "SERVICE[${SERVICE}] TYPE[${TYPE}]"|${T} [:lower:] [:upper:]
	
	FUNCTIONS=($(${E} "__all__" ${CHAOSDIR}/${SERVICE}/${TYPE}.py | \
			${S} -n -E "s/^.*\[(.*)\]/\1/p" | \
			${S} -E "s/(\"|'|,)//g"))

	if [ -z ${FUNCTIONS} ]; then
		MULTILINE=$(${S} -n -E "/__all__/,/\]/p" ${CHAOSDIR}/${SERVICE}/${TYPE}.py)
		FUNCTIONS=($(echo ${MULTILINE}|${S} -n -E "s/^.*\[(.*)\]/\1/p"|${S} -E "s/(\"|'|,)//g"))
	fi

	for func in ${FUNCTIONS[@]}; do
		echo -e "\t- ${func}"
		# Now we print the parameters the function takes
		${S} -n "/def ${func}(/,/)/ {s/def ${func}//;s/^ */\t\t/p}" ${CHAOSDIR}/${SERVICE}/${TYPE}.py
	done
	echo
done;
