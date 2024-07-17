# Commands for interacting with the Near-RT RIC Kubernetes Cluster

## Listing active Kubernetes pods

```bash
# List Kubernetes pods in all namespaces
kubectl get pods -A
```

```bash
# List Kubernetes pods in a given namespace
kubectl get pods -n <namespace>
```

```bash
# Example to list all running xApp pods
kubectl get pods -n ricxapp
```

## Describing information about active Kubernetes pods

```bash
kubectl describe pod <pod_name> -n <namespace>
```

```bash
# Example to describe info a given xApp
kubectl describe pod ricxapp-examplexapp-6867f6c785-9pvc5 -n ricxapp
```

## Printing Logs

```bash
# Print the log/stdout of a given pod
kubectl logs <pod_name> -n <namespace>
```

```bash
# Example of the log command for an xApp
kubectl logs ricxapp-examplexapp-6867f6c785-9pvc5 -n ricxapp
```

# Inspecting active Kubernetes services 
```bash
# List esposed services and open ports
kubernetes get services -A
```

```bash
# Send HTTP/REST request
curl -X GET <xapp_IP>:<xapp_port>/<path>
```

```bash
# Example of HTTP/REST request
curl -X GET 10.107.57.43:8080/ric/v1/health
```

# Inspecting Storage Class

```bash
# List the configured storage classes
kubectl get storageclass -A
```

```bash
# List the configured persistent volumes
kubectl get pv -A
```

# Openning Shell to active Kubernetes pod

```bash
# Open shell to a given pod in the cluster
kubectl exec -it <pod_name> -n <namespace> -- /bin/bash
```

```bash
# Example to open a shell to the DBaaS pod
kubectl exec -it statefulset-ricplt-dbaas-server-0 -n ricplt -- /bin/bash
```
