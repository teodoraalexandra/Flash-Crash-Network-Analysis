$persons = $args[0]
$informed = $args[1]

docker run -it -v ${PWD}\results:/app/results flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed"