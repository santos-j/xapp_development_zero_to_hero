## Commands for building xApp Docker images

```bash
# Build xApp image with a name and tag
docker build <DOCKERFILE_PATH> -t <REGISTRY_HOSTNAME>:<REGISTRY_PORT> <XAPP_NAME>:<XAPP_TAG> --network host
```

```bash
# Example using a local Docker Registry
docker build . -t localhost:5001/test_xapp:1.0.0 --network host
```

## Commands for pushing xApp Docker images to a Docker Registry

```bash
# Push the xApp image to Docker Registry
docker push <REGISTRY_HOSTNAME>:<REGISTRY_PORT> <XAPP_NAME>:<XAPP_TAG> 
```

```bash
# Example using a local Docker Registry
docker push localhost:5001/example_xapp:1.0.0
```

## Commands for running a local Docker Registry

```bash
# Run a self-restarting Docker Registry
docker run -d -p <REGISTRY_PORT>:5000 --restart unless-stopped --name <REGISTRY_NAME> registry:2  
```

```bash
# Example using port 5001
docker run -d -p 5001:5000 --restart unless-stopped --name registry registry:2  
```
## Commands for inspecting a Docker Registry

```bash
# Check Docker images stored locally
docker image ls 
```

```bash
# Query the available images in a Registry
curl -X GET http://<REGISTRY_HOSTNAME>:<REGISTRY_PORT>/v2/_catalog
```

```bash
# Example of query to a local Registry
curl -X GET http://localhost:5001/v2/_catalog  
```
