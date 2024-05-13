$GREEN = "`033[0;32m"

$persons = $args[0]
$informed = $args[1]

Write-Host "${GREEN}Building new Docker image..."
docker build -t flash-crash-ntw-anls:latest .
Write-Host "${GREEN}Starting docker container and running execution..."
docker run -it --rm flash-crash-ntw-anls:latest ./script.sh "$persons" "$informed"
