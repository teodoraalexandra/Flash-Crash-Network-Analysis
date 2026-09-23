$persons= $args[0]
$informed= $args[1]
$aggressivity= $args[2]
$threshold= $args[3]
$risk_limit= $args[4]

docker run -it -v ${PWD}\results:/app/results information-asymmetry-networks:latest ./script.sh "$persons" "$informed" "$aggressivity" "$threshold" "$risk_limit"
