Testing the Helm Deployment Locally
With microk8s and Helm:

Check your chart is valid:

bash
Copy code
cd ~/multi-tenant-kv-store/helm
microk8s helm3 template . --namespace default
If you see “Error: YAML parse error…” fix any indentation or references.
Install/Upgrade:

bash
Copy code
microk8s helm3 upgrade --install mt-kv-store . \
  --namespace default \
  --set image.repository=adesojialu/multitenant \
  --set image.tag=latest
Wait for pods:

microk8s helm3 status mt-kv-store --namespace default

kubectl get pods -n default
NAME                                             READY   STATUS    RESTARTS   AGE
multi-tenant-kv-store-fastapi-64fffc4859-nfn9p   1/1     Running   0          3m26s
multi-tenant-kv-store-huey-8f957f448-qrjdm       1/1     Running   0          3m26s
redis-86778467d4-fkpdd                           1/1     Running   0          3m26s
adesoji@adesoji-Lenovo-Legion-7-15IMH05:~/multi-tenant-kv-store/helm$ kubectl get services -n default
NAME                            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes                      ClusterIP   10.152.183.1     <none>        443/TCP    17h
multi-tenant-kv-store-fastapi   ClusterIP   10.152.183.87    <none>        8000/TCP   3m42s
redis                           ClusterIP   10.152.183.106   <none>        6379/TCP   3m42s


bash``
Copy code
microk8s kubectl get pods -n default
Check logs:

bash
Copy code
microk8s kubectl logs deployment/mt-kv-store -n default
Port-forward or define a NodePort to test your endpoints:

kubectl port-forward service/multi-tenant-kv-store-fastapi 8000:8000 -n default
bash
Copy code
microk8s kubectl port-forward deployment/mt-kv-store 8000:8000 -n default
Curl:

bash
Copy code
curl -X POST http://127.0.0.1:8000/auth/signup ...


microk8s helm3 upgrade --install mt-kv-store .   --namespace default   --set image.repository=adesojialu/multitenant   --set image.tag=latest
Release "mt-kv-store" has been upgraded. Happy Helming!
NAME: mt-kv-store
LAST DEPLOYED: Mon Jan 13 15:55:58 2025
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
adesoji@adesoji-Lenovo-Legion-7-15IMH05:~/multi-tenant-kv-store/helm$ microk8s kubectl get pods -n default
NAME                                              READY   STATUS    RESTARTS       AGE
multi-tenant-kv-store-79fbff8564-wvn74            1/1     Running   0              53s
multi-tenant-kv-store-79fbff8564-xv2wj            1/1     Running   0              53s
my-graf-grafana-7bf4bcd9b4-lskck                  1/1     Running   1 (170m ago)   3h18m
my-prom-alertmanager-0                            0/1     Pending   0              3h24m
my-prom-kube-state-metrics-b89c88f47-4b6qd        1/1     Running   1 (170m ago)   3h24m
my-prom-prometheus-node-exporter-q5495            1/1     Running   1 (170m ago)   3h24m
my-prom-prometheus-pushgateway-599c89cdb9-k55cz   1/1     Running   1 (170m ago)   3h24m
my-prom-prometheus-server-645b8b586d-ss5cw        0/2     Pending   0              3h24m
adesoji@adesoji-Lenovo-Legion-7-15IMH05:~/multi-tenant-kv-store/helm$ microk8s kubectl logs deployment/mt-kv-store -n default
error: error from server (NotFound): deployments.apps "mt-kv-store" not found in namespace "default"
adesoji@adesoji-Lenovo-Legion-7-15IMH05:~/multi-tenant-kv-store/helm$ microk8s kubectl logs multi-tenant-kv-store-79fbff8564-wvn74 -n default
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)


)
adesoji@adesoji-Lenovo-Legion-7-15IMH05:~/multi-tenant-kv-store/helm$ microk8s kubectl port-forward pod/multi-tenant-kv-store-79fbff8564-wvn74 8000:8000 -n default
Forwarding from 127.0.0.1:8000 -> 8000
Forwarding from [::1]:8000 -> 8000
Handling connection for 8000
Handling connection for 8000
Handling connection for 8000


helm repo update























Stopping All Existing Pods & Fresh Deploy
If you want to remove everything and start fresh:

List your current Helm releases:
bash
Copy code
microk8s helm3 list -n default
Uninstall your release:
bash
Copy code
microk8s helm3 uninstall mt-kv-store -n default
Confirm pods are gone:
bash
Copy code
microk8s kubectl get pods -n default
Reinstall:
bash
Copy code
microk8s helm3 upgrade --install mt-kv-store . -n default \
  --set image.repository=adesojialu/multitenant \
  --set image.tag=latest
Now you have a fresh deployment with your updated config.

6. What to Expect Next
Redis logs in its own Pod (unless you’re using an external Redis).
Huey logs in a separate Pod if you define a huey deployment.
Uvicorn logs in the mt-kv-store pods.
Metrics accessible at GET /metrics from your FastAPI container(s).
If you have Prometheus installed, it scrapes them automaticall



microk8s kubectl delete pods --all -n default
microk8s kubectl delete all --all -n default
microk8s kubectl delete all --all --all-namespaces
#verify
microk8s kubectl get pods -n default
microk8s kubectl get pods -n default -w


 microk8s helm3 list -n default
 microk8s helm3 uninstall mt-kv-store -n default
 microk8s kubectl get secrets -n default
  microk8s kubectl get secrets -n default






  Below is a **step-by-step** guide on how to **delete all previous Helm deployments**, **remove leftover resources**, and **run a fresh deployment**. Finally, we’ll show you how to **curl** your FastAPI app on port 8000 to confirm it’s working.

---

## 1. **List All Helm Releases**

First, see which Helm releases are installed in the default namespace:

```bash
microk8s helm3 list -n default
```
You might see something like:
```
NAME                 	NAMESPACE 	REVISION UPDATED   STATUS   CHART
multi-tenant-kv-store default    3        ...       deployed multi-tenant-kv-store-0.1.0
my-prom               default    1        ...       deployed prometheus-...
my-graf               default    1        ...
...
```

---

## 2. **Uninstall (Delete) the Old Release**

If your old release is named `multi-tenant-kv-store`:

```bash
microk8s helm uninstall multi-tenant-kv-store -n default
```
This removes the Helm release and *most* of its resources.

Sometimes, if there were leftover resources that **were not** owned by that release (like a leftover secret or changed resources), you may still have them in the cluster. Check:

```bash
microk8s kubectl get all -n default
microk8s kubectl get secrets -n default
```

If you see leftover resources named something like `multi-tenant-kv-store-secret` or old deployments that remain, delete them manually:

```bash
microk8s kubectl delete secret multi-tenant-kv-store-secret -n default
microk8s kubectl delete deployment multi-tenant-kv-store-fastapi -n default
microk8s kubectl delete deployment multi-tenant-kv-store-huey -n default
microk8s kubectl delete deployment multi-tenant-kv-store-redis -n default
```

**Now** your cluster is fully cleared of old resources.

---

## 3. **Run a Fresh Deployment in Helm**

After removing old leftover resources, you can do a fresh install:

```bash
cd /path/to/your/helm/chart   # e.g. "my-chart"
microk8s helm3 upgrade --install mt-kv-store . \
  --namespace default \
  --set image.repository=adesojialu/multitenant \
  --set image.tag=latest
```

- `--install` means if the release doesn’t exist, create it.  
- `mt-kv-store` is the new release name.  
- If you have any custom sets, you can pass them as well.

---

## 4. **Check the New Deployment**

```bash
microk8s kubectl get pods -n default
```
You should see:
```
NAME                                          READY  STATUS    RESTARTS  AGE
mt-kv-store-fastapi-xxx                       1/1    Running   0         ...
mt-kv-store-huey-xxx                          1/1    Running   0         ...
mt-kv-store-redis-xxx                         1/1    Running   0         ...
```

---

## 5. **Port-Forward to Curl on Port 8000**

If you want to test the FastAPI app locally:

1. **Identify** the name of the FastAPI pod or service. For instance, if your service is named `mt-kv-store-fastapi`, you could do:

   ```bash
   microk8s kubectl port-forward service/mt-kv-store-fastapi 8000:8000 -n default
   or 

   kubectl port-forward service/multi-tenant-kv-store-fastapi 8000:8000 -n default

   ```
   or if you have a single **pod** and want to port-forward that:

   ```bash
   microk8s kubectl port-forward deployment/mt-kv-store-fastapi 8000:8000 -n default
   ```

2. **Curl** from your local machine:

   ```bash
   curl http://127.0.0.1:8000
   ```
   or if you have a health endpoint:
   ```bash
   curl http://127.0.0.1:8000/health
   ```

If everything is correct, you see a success response (like `{"status":"ok"}` if you coded a health endpoint) or your FastAPI docs page if you request `/docs`.

---

## 6. **Summary**

1. **Uninstall** old releases with `microk8s helm3 uninstall <release> -n default`.  
2. **Remove** any leftover resources manually (`kubectl delete secret...`, `kubectl delete deployment...`) if they still remain.  
3. **Install** fresh with `microk8s helm3 upgrade --install mt-kv-store . -n default ...`.  
4. **Check** pods to ensure they are running.  
5. **Port-forward** to the FastAPI service or deployment on port 8000, then `curl localhost:8000`.

By following these steps, you’ll have a clean environment and can verify your FastAPI application with no leftover conflicts.

microk8s helm3 uninstall mt-kv-store -n default

microk8s kubectl get secrets -n default
microk8s kubectl delete secret multi-tenant-kv-store-secret -n default