```

  python -m huey.bin.huey_consumer src.services.tasks.huey  or    python -m huey.bin.huey_consumer src.services.tasks.huey --logfile=huey.log

uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2 --reload

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm install my-prom prometheus-community/prometheus
helm install my-graf grafana/grafana

cd /home/adesoji/Documents/cambsubmission/multi-tenant-kv-store
docker rmi $(docker images -q)
docker volume prune -f

docker container prune -f

docker system prune -a -f --volumes

docker build --no-cache -t adesojialu/multitenant:latest .

docker login
echo Authenticating with existing credentials...
WARNING! Your password will be stored unencrypted in /home/adesoji/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credential-stores

docker push  adesojialu/multitenant:latest
```
psql "postgresql://postgres:%23%40%40dfyttyy55464As@db.qxyxszjvfffbvrmsdcxt.supabase.co:5432/postgres

docker build --no-cache -t adesojialu/hueyimage:latest -f Dockerfile.huey .
docker push adesojialu/hueyimage:latest

docker build --no-cache -t adesojialu/locust:latest -f Dockerfile.locust .

docker push adesojialu/locust:latest



https://github.com/coleifer/huey/blob/master/examples/simple/tasks.py

$ uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2 --reload

python -m huey.bin.huey_consumer src.services.tasks.huey 

locust -f locustfile.py --host=http://localhost:8000 --users=500 --spawn-rate=50 --run-time=20s




TOKEN=<PASTE_YOUR_ACCESS_TOKEN_HERE>

curl -X POST http://localhost:8000/kv/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"key": "myKey", "value": "hello world", "ttl": 60}'




Test Key-Value Operations Again:

After ensuring Redis is running correctly and PostgreSQL is connected, perform key-value operations via your API endpoints and verify their effects in Redis CLI.



Testing Endpoints with curl
Use curl, HTTPie, Postman, or Insomnia to interact with your API endpoints. Here's how to do it with curl.

2.2.1. Sign Up a New Tenant
bash```

curl -X POST http://localhost:8000/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"secret123"}'
```
```
Expected Behavior:

Uvicorn Logs (Terminal #1):


INFO:     127.0.0.1:XXXX - "POST /auth/signup HTTP/1.1" 200 OK
PostgreSQL:
```

```
A new entry in the public.tenants table.
A new schema named tenant_<id> created.
Response:

json

{
  "message": "Tenant created with ID: 1"
}
```
 Log In to Obtain Access Token
bash```

curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test@example.com&password=secret123"
```
```
Expected Behavior:

Uvicorn Logs (Terminal #1):


INFO:     127.0.0.1:XXXX - "POST /auth/login HTTP/1.1" 200 OK
Response:

json
Copy code
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
Note: Save the access_token for authenticated requests.


Create:

bash```
Copy code
TOKEN=<YOUR_ACCESS_TOKEN>

curl -X POST http://localhost:8000/kv/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"key": "myKey", "value": "hello world", "ttl": 60}'
```

Read:

bash```

curl -X GET http://localhost:8000/kv/myKey \
     -H "Authorization: Bearer $TOKEN"
```

Update:

bash```
curl -X PUT http://localhost:8000/kv/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"key": "myKey", "value": "updated value"}'
``` 

Delete:

bash```
curl -X DELETE http://localhost:8000/kv/myKey \
     -H "Authorization: Bearer $TOKEN"
```





1.2 Build & Run the Application Locally
Build & Start all containers:

bash
Copy code
docker-compose up --build
This will:

Build your FastAPI image (using the Dockerfile).
Start the web (FastAPI), db (Postgres), and redis (Redis) containers.
Check Logs:
You’ll see logs in your terminal for FastAPI, Postgres, and Redis.

If everything is successful, you’ll see something like:
perl
Copy code
web       | INFO:     Uvicorn running on http://0.0.0.0:8000
db        | LOG:  database system is ready to accept connections
redis     | 1:M  ... Ready to accept connections
Access FastAPI:
Open your browser to http://localhost:8000.

For example, check [GET] /docs or [GET] /metrics if you’ve enabled the Prometheus instrumentator.
Run Huey (Separate Container, Optional):
If you’ve added a huey-worker service in docker-compose.yaml, run:

bash
Copy code
docker-compose up --build huey-worker
or if it’s included in the default docker-compose up, it will also start automatically.

Alternatively, for dev, some folks prefer to run Huey in a separate terminal:
bash
Copy code
python -m huey.bin.huey_consumer src.services.tasks.huey --loglevel=info
Redis CLI:

If you want to enter the Redis container and use redis-cli:
bash
Copy code
docker exec -it mt_redis sh
# now inside container
redis-cli
# You can run commands like: KEYS *
Or from your host (if installed locally):
bash
Copy code
redis-cli -h 127.0.0.1 -p 6380
Stop everything:

Press Ctrl+C in the terminal where docker-compose is running.
Or run docker-compose down.
2. Building & Pushing Docker Image
If you want to push your image to Docker Hub (e.g., adesojialu/multitenant:latest), follow these steps:

Login (if you haven’t):
bash
Copy code
docker login
Build your image (tagging with your Docker Hub repo):
bash
Copy code
docker build -t adesojialu/multitenant:latest .
Push:
bash
Copy code
docker push adesojialu/multitenant:latest
Verify on Docker Hub.
Now your image is available to pull from any environment (like microk8s or a cloud-based K8s).
3. Deploying on microk8s with Helm
3.1 Prerequisites
microk8s installed and running.
Helm installed (often via microk8s enable helm3 or you can install the Helm binary separately).
You have your Docker image in a registry accessible by microk8s (e.g., Docker Hub).
3.2 Steps to Deploy
Enable features in microk8s (if not already):

bash
Copy code
microk8s enable dns rbac helm3
Add your Docker registry credentials if needed (for pulling private images), or use a public registry.

Navigate to your Helm chart folder:

bash
Copy code
cd helm
Install/Upgrade your chart in a namespace (e.g., default or create a new one):

bash
Copy code
microk8s helm3 upgrade --install mt-kv-store . \
  --namespace default \
  --set image.repository=adesojialu/multitenant \
  --set image.tag=latest
This will create:
A Deployment for your FastAPI service,
A Service (ClusterIP by default),
A Secret for sensitive environment variables,
Optional HPA if configured,
etc.
Check the pods:

bash
Copy code
microk8s kubectl get pods -n default
You should see something like:

sql
Copy code
NAME                                  READY   STATUS    RESTARTS   AGE
mt-kv-store-abc123-xyz456            1/1     Running   0          30s
Check logs or describe the pod if needed:

bash
Copy code
microk8s kubectl logs mt-kv-store-abc123-xyz456 -n default
Check the Service to see if it’s exposed or if you need to port-forward:

bash
Copy code
microk8s kubectl get svc -n default
If it’s ClusterIP, you can do a port-forward to your local:
bash
Copy code
microk8s kubectl port-forward deployment/mt-kv-store 8000:8000 -n default
Then open http://localhost:8000/docs or http://localhost:8000/metrics.
4. Checking Metrics, Pods, and Health
Metrics:

If you used prometheus-fastapi-instrumentator, your app exposes /metrics.
You can view it directly in a browser by port-forwarding or by specifying an Ingress.
If you install Prometheus (via Helm or microk8s), configure it to scrape that endpoint.
Pods:

microk8s kubectl get pods -n default
microk8s kubectl describe pod <pod-name> -n default
Health Probes:

Liveness and readiness probes are defined in your deployment.yaml, e.g.:
yaml
Copy code
readinessProbe:
  httpGet:
    path: /auth/login
    port: 8000
You can check the status in kubectl describe pod <pod-name>:
yaml
Copy code
Liveness probe failed: ...
Readiness probe succeeded ...
5. Huey on microk8s
If you want Huey running as a separate Deployment, you can:

Create a new YAML or add a second Deployment in your Helm chart (e.g., huey-deployment.yaml):
yaml
Copy code
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mt-kv-store-huey
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mt-kv-store-huey
  template:
    metadata:
      labels:
        app: mt-kv-store-huey
    spec:
      containers:
        - name: huey-worker
          image: "adesojialu/multitenant:latest"
          command: ["python", "-m", "huey.bin.huey_consumer", "src.services.tasks.huey", "--loglevel=info"]
          env:
            # same environment variables as your main app
            # so it can connect to Redis, Postgres if needed
Install it via Helm or kubectl apply -f huey-deployment.yaml.
Check logs to confirm it’s processing tasks:
bash
Copy code
microk8s kubectl logs deployment/mt-kv-store-huey
Redis typically is also in Kubernetes or external. If you rely on the same Redis inside microk8s, you can run a redis chart or any managed Redis solution.
6. Summary of Commands
Below is a quick reference:

Local Docker Compose:
bash
Copy code
docker-compose up --build
# Shut down
docker-compose down
Local Docker (manual):
bash
Copy code
docker build -t <youruser>/<imagename>:latest .
docker run -p 8000:8000 <youruser>/<imagename>:latest
Push to Docker Hub:
bash
Copy code
docker login
docker push <youruser>/<imagename>:latest
microk8s + Helm (assuming your chart is in helm/):
bash
Copy code
cd helm
microk8s helm3 upgrade --install mt-kv-store . -n default \
  --set image.repository=<youruser>/<imagename> --set image.tag=latest
microk8s kubectl get pods -n default
microk8s kubectl port-forward deployment/mt-kv-store 8000:8000 -n default
Check logs:
bash
Copy code
microk8s kubectl logs deployment/mt-kv-store -n default
Check metrics:
If you’ve port-forwarded, open a browser at http://localhost:8000/metrics.
If you have Prometheus installed, configure it to scrape that endpoint.




cd /home/adesoji/multi-tenant-kv-store/helm  # or wherever your chart is
microk8s helm3 upgrade --install mt-kv-store . \
  --namespace default \
  --set image.repository=adesojialu/multitenant \
  --set image.tag=latest

Check if pods are running:
bash```
microk8s kubectl get pods
```
Check logs for your main app:
bash```

microk8s kubectl logs deployment/mt-kv-store -f
```
(Optional) If you have a separate Huey deployment, logs might be in deployment/huey-worker.
4. Prometheus & Grafana Setup
You’ve already installed Prometheus and Grafana with:

bash```
helm install my-prom prometheus-community/prometheus
helm install my-graf grafana/grafana
So you have:

Prometheus scraping your cluster.
Grafana installed for dashboards.
4.1 Exposing Metrics with FastAPI
In main.py, you have:

python
Copy code
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
And in your Helm deployment.yaml, you have annotations:

yaml```
Copy code
prometheus.io/scrape: "true"
prometheus.io/port: "8000"
prometheus.io/path: "/metrics"
What This Means:

Prometheus will scrape the "/metrics" endpoint on port 8000.
You can see all your FastAPI-related metrics (requests count, latency histograms, error rates, etc.) in Prometheus.
```
4.2 Accessing Prometheus
From the info you posted:

Prometheus server is running inside the cluster.
You can do a port forward to your local machine:
bash```

export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=my-prom" -o jsonpath="{.items[0].metadata.name}")
```
bash```
kubectl --namespace default port-forward $POD_NAME 9090
```
Then open http://localhost:9090 to see the Prometheus UI.
4.3 Accessing Grafana
Similar approach:

bash
Copy code
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=my-graf" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace default port-forward $POD_NAME 3000
Visit http://localhost:3000.
Login with the admin user, password from kubectl get secret --namespace default my-graf-grafana ... | base64 --decode.
4.4 What You’ll See in /metrics
When you open the endpoint or query in Prometheus, you’ll see something like:

http_request_duration_seconds_count
http_request_duration_seconds_sum
http_request_duration_seconds_bucket
http_request_size_bytes_count, etc.
Each metric typically has labels for path, method, status code, etc. For example:

lua
Copy code
http_request_duration_seconds_bucket{le="0.003",method="GET",path="/kv/{key}",status_code="200"} 15
...
This shows how many requests to /kv/{key} completed in under 0.003 seconds, etc.

In Grafana, you can build dashboards that visualize these metrics (requests per second, latencies, error rates).



echo -n 'CHANGE_ME_SUPER_SECRET' | base64
echo -n "postgresql://postgres:#@@dfyttyy55464As@db.qxyxszjvfffbvrmsdcxt.supabase.co:5432/postgres" | base64

echo -n "db.qxyxszjvfffbvrmsdcxt.supabase.co" | base64

echo -n "#@@dfyttyy55464As" | base64

echon -n "postgres" | base64




microk8s kubectl delete all --all -n default
microk8s kubectl get all -n default


References


https://sayanc20002.medium.com/fastapi-multi-tenancy-bf7c387d07b0

https://medium.com/@het.trivedi05/designing-multi-tenant-applications-on-kubernetes-f0470f8e641c

https://huey.readthedocs.io/en/0.4.9/consumer.html

https://stackoverflow.com/questions/67720625/kubernetes-liveness-probe-httpget-schema-not-working-correctly

https://github.com/planktonzp/kubernetes-redis-cluster/blob/master/redis-cluster-debug.yml

https://abdelrhmanhamouda.github.io/locust-k8s-operator/#at-a-glance

https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

https://signoz.io/guides/how-do-i-monitor-api-in-prometheus/



docker build  --no-cache  -t adesojialu/hueyimage:latest -f Dockerfile.huey .

docker push  adesojialu/hueyimage:latest

docker build  --no-cache  -t adesojialu/multitenant:latest -f Dockerfile .

docker push  adesojialu/multitenant:latest






## Short Architecture Document

### **Design Justifications**

#### **Redis Topology**
- **Replication Strategy**: A Redis cluster was chosen for horizontal scalability and fault tolerance. Each node in the cluster manages a subset of keys, ensuring even data distribution and reducing bottlenecks.
  - **Reason**: Redis clustering supports sharding, making the system capable of handling high throughput (e.g., 10k reads/writes per second).
  - **Replication**: Each shard has replicas for failover, ensuring high availability.

#### **FastAPI Application**
- **Horizontal Scaling**: The FastAPI application is deployed with multiple replicas managed by Kubernetes.
  - **Reason**: Multiple replicas ensure the system can handle increased user load and failover scenarios.
- **JWT-Based Authentication**: Ensures secure and isolated access for tenants. Each tenant’s data is namespaced to prevent collisions.

#### **Huey Integration**
- **Background Tasks**: Huey handles periodic tasks like removing expired keys and logging operations asynchronously.
  - **Reason**: Offloading these tasks ensures that user-facing endpoints remain responsive.

#### **Monitoring**
- **Prometheus and Grafana**:
  - Prometheus scrapes metrics exposed by the FastAPI app and Huey.
  - Grafana visualizes these metrics, providing insights into request rates, task queue sizes, and system latency.

### **Architecture Diagram**
```mermaid
graph TD
    subgraph Kubernetes Cluster
        A[FastAPI Application] -- CRUD Operations --> C[Redis Cluster]
        A -- Metrics --> D[Prometheus]
        B[Huey Workers] --> C
        C -- Replication --> C
    end
    D -- Visualization --> E[Grafana]
    F[Clients] --> A
```

### **Multi-Region Setup**
- **Objective**: Ensure low latency and high availability for global users.
- **Strategy**:
  - **Data Replication**: Use Redis’s cross-region replication feature to synchronize clusters across regions.
  - **Traffic Routing**: Use a global load balancer to route users to the nearest regional cluster.
  - **Consistency**:
    - Implement a write-forwarding mechanism to ensure consistency for write operations.
    - Use eventual consistency for read-heavy workloads to optimize performance.

### **Advanced Scaling Scenarios**
#### **Auto-scaling**
- Enable Kubernetes Horizontal Pod Autoscaler (HPA) for FastAPI and Huey pods based on CPU/memory usage and custom metrics (e.g., request rate).

#### **Sharding Improvements**
- Dynamically adjust Redis shards based on data growth patterns using a monitoring service.

### **Potential Improvements**

#### **Caching Layers**
- **Integration**: Add a local caching layer (e.g., Memcached) for frequently accessed keys.
- **Benefit**: Reduces load on Redis, improving response times.

#### **Advanced Load Testing**
- Use tools like Locust or k6 to simulate large-scale user traffic.
- Identify bottlenecks and optimize critical paths.

#### **Zero-Downtime Deployments**
- **Blue-Green Deployment**: Deploy new versions of services alongside the existing ones and gradually switch traffic.
- **Canary Releases**: Test changes with a small percentage of users before full rollout.

#### **Disaster Recovery**
- Implement backup and restore mechanisms for the Redis cluster and PostgreSQL database.
- Store backups in a secure and geographically redundant storage solution (e.g., AWS S3).

---

docker run -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus


docker run \
  -p 3000:3000 \
  -v $(pwd)/grafana.yml:/etc/grafana/grafana.yml \
  -v $(pwd)/datasources:/etc/grafana/provisioning/datasources \
  -v $(pwd)/dashboards:/var/lib/grafana/dashboards \
  grafana/grafana

docker run -p 9090:9090  --add-host=host.docker.internal:host-gateway -v /etc/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus


docker run -p 3000:3000   -v /etc/grafana/provisioning:/etc/grafana/provisioning   -v /var/lib/grafana/dashboards:/var/lib/grafana/dashboards   grafana/grafana



adesoji@adesoji-Lenovo-Legion-7-15IMH05:~/Documents/cambsubmission/multi-tenant-kv-store$ docker run -d -p 3000:3000   -v /home/adesoji/Documents/cambsubmission/multi-tenant-kv-store/grafana.ini:/etc/grafana/grafana.ini   -v /etc/grafana/provisioning:/etc/grafana/provisioning   -v /var/lib/grafana/dashboards:/var/lib/grafana/dashboards   grafana/grafana




docker run -d -p 3000:3000 \
  -v /home/adesoji/grafana.ini:/etc/grafana/grafana.ini \
  -v /home/adesoji/grafana/provisioning:/etc/grafana/provisioning \
  -v /home/adesoji/grafana/dashboards:/var/lib/grafana/dashboards \
  grafana/grafana


docker run  -d -p 3000:3000   -v /home/adesoji/Documents/cambsubmission/multi-tenant-kv-store/grafana.ini:/etc/grafana/grafana.ini -v /home/adesoji/grafana/provisioning:/etc/grafana/provisioning   -v /home/adesoji/grafana/dashboards:/var/lib/grafana/dashboa
rds   grafana/grafana


docker exec -it 68f8642c9723 grafana-cli plugins install alexanderzobnin-zabbix-app
   
Deprecation warning: The standalone 'grafana-cli' program is deprecated and will be removed in the future. Please update all uses of 'grafana-cli' to 'grafana cli'
✔ Downloaded and extracted alexanderzobnin-zabbix-app v4.6.1 zip successfully to /var/lib/grafana/plugins/alexanderzobnin-zabbix-app

Please restart Grafana after installing or removing plugins. Refer to Grafana documentation for instructions if necessary.


docker run -p 9090:9090  --add-host=host.docker.internal:host-gateway -v /etc/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus