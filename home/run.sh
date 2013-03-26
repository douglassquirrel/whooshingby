start() {
  DIRECTORY="$1"
  EXECUTABLES=( `find $DIRECTORY -maxdepth 1 -executable -type f` )
  if [ ${#EXECUTABLES[@]} -ne 1 ]
  then
    echo "Cannot locate unique executable in directory $DIRECTORY"
    exit 1
  fi
  EXECUTABLE=`basename ${EXECUTABLES[0]}`
  ( cd $DIRECTORY && ./$EXECUTABLE & )
}

start task-submit-html
python ./server.py