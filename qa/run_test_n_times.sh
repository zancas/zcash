#! /usr/bin/env bash


USAGE='Usage: runtest_n_times -n $NUMBEROFRUNS -r $REPO -t $TEST'

USAGE2='This utility runs an RPC test (-t) from a particular repository (-r) for a certain (-n)
number of iterations. It aims to fail informatively, and provide a useful output format.

In particular output is written to a sibling of the targeted repository.  The log is stored under:

REPOPARENT/looplogs/TESTNAME/REPONAME/BRANCHNAME_COMMITHASH.log

The timestamp at the beginning of each invocation is stored inside the log file.

This tool supports abort by a single invocation of "Ctrl-C".'

if [[ "$@" == *"-h"* ]]
then
      echo $USAGE
      echo
      echo $USAGE2
      exit 10
fi

if [ "$#" -ne 6 ]
then
    echo There must be exactly 6 arguments, 3 parameters and their values.
    echo $USAGE
    echo
    echo $USAGE2
    exit 11
fi

OPTIND=1
while getopts "n:r:t:" arg
do
    case "${arg}" in
        n  )
            if [[ $OPTARG =~ ^[0-9]+$ ]]
            then
                ITERATIONS=${OPTARG};
            else
                echo \"${OPTARG}\" was entered as a value for "-n", but "-n"
                echo is the number of iterations and must be a positive integer.
                echo ${USAGE}
                exit 12
            fi
            ;;
    esac
done
OPTIND=1
while getopts "n:r:t:" arg
do
    case "${arg}" in
        r  )
            REPO_NAME=$(ls -1 `pwd` | grep -e"^${OPTARG}$" || true);
            if [ -z "$REPO_NAME" ]
            then
                echo The named repo: ${OPTARG}
                echo isn\'t in 
                echo ${USAGE}
                exit 13
            fi
            pushd ${REPO_NAME} > /dev/null && git rev-parse --short HEAD > /dev/null;
            if [ $? -ne 0 ]
            then
                echo The named directory: ${OPTARG}
                echo doesn\'t seem to be a git repo.
                echo ${USAGE}
                popd
                exit 14
            fi
            popd > /dev/null
            ;;
    esac
done
OPTIND=1
while getopts "n:r:t:" arg
do
    case "${arg}" in
        t  )
            TEST_NAME=$(ls -1 ./${REPO_NAME}/qa/rpc-tests/ | grep ${OPTARG} || true);
            if [ -z "$TEST_NAME" ]
            then
                echo The named test: ${OPTARG}
                echo isn\'t in "${REPO_NAME}/qa/rpc-tests"
                echo ${USAGE}
                exit 15
            fi
            ;;
        \? )
            echo ${USAGE}
            exit 16
    esac
done

function main () {
    LOGDIRNAME=`pwd`/looplogs/$TEST_NAME/$REPONAME;
    mkdir -p $LOGDIRNAME;
    # I need to be in the repo context to use git
    pushd ./$REPO_NAME > /dev/null \
        && LOGBASENAME="`git branch --show`_`git rev-parse HEAD`.log" \
        && popd > /dev/null;

    LOGFILE=$LOGDIRNAME/$LOGBASENAME;
    echo "This run started at: " >> $LOGFILE;
    date "+%s" >> $LOGFILE;
    ZCASHDVERSION=`./$REPO_NAME/src/zcashd --version`
    echo "The zcashd version is: ${ZCASHDVERSION}" >> ${LOGFILE};
    let count=1;
    while [ $count -le $ITERATIONS ];
    do
        rm -rf .lock blocks cache chainstate database db.log debug.log zcashd.pid \
        && ./$REPO_NAME/qa/pull-tester/rpc-tests.sh $TEST_NAME >> $LOGFILE 2>&1 ; LASTPID=$! \
        && count=$(( $count + 1 ))
    done
    rm -rf .lock blocks cache chainstate database db.log debug.log zcashd.pid
}

control_c() {
    kill $LASTPID
    exit 18
}

trap control_c SIGINT

main
