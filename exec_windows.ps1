# Used for custom runs
# $persons = $args[0]
# $informed = $args[1]

$persons = 1000
$informed = 2

docker run -it -v ${PWD}\results:/app/results flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed"
