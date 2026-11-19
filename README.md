# Student Management System - Microservices, Docker & Kubernetes

**Student:** Khorn Sokhadom  
**2nd microservice:** Update student mobile number or password

## Architecture

```
Postman ──► student-gateway-service (NodePort 30090)
              │
   ┌──────────┴──────── Pod 1: gateway-registration-pod ─────────┐
   │  api-gateway :8080  ──localhost──►  registration-service :5001 │
   └──────────┬─────────────────────────────────────────────────────┘
              │ http://update-service:5002 (ClusterIP)
   ┌──────────┴──────── Pod 2: update-pod ────┐
   │  update-service :5002                     │
   └───────────────────────────────────────────┘
                 both services ──► MongoDB Atlas (collection: students)
```

Database schema (`students` collection):
`Student_id, Student_name, student_mobile, student_email, student_password` (password stored as a bcrypt hash).

## API (all calls go through the API Gateway)

| Method | Path | Microservice |
|---|---|---|
| POST | `/api/register` | Registration |
| GET | `/api/students` | Registration |
| GET | `/api/students/:id` | Registration |
| PUT | `/api/update/mobile/:id` | Update |
| PUT | `/api/update/password/:id` | Update |
| PATCH | `/api/update/:id` (mobile and/or password) | Update |

Register body:
```json
{ "student_name": "Khorn Sokhadom", "student_mobile": "012345678", "student_email": "sokhadom@student.edu", "student_password": "pass1234" }
```

## Project structure

```
api-gateway/            server.js, Dockerfile
registration-service/   server.js, db.js, student_schema.js, counter_schema.js, Dockerfile
update-service/         server.js, db.js, student_schema.js, Dockerfile
k8s/pods.yaml           2 Pods (Pod 1: gateway + registration, Pod 2: update)
k8s/services.yaml       student-gateway-service (NodePort) + update-service (ClusterIP)
k8s/secret.example.yaml MongoDB secret template
postman/                Postman collection
```

## Run on Minikube

1. Put your MongoDB connection string in a `.env` file in the project root (see `.env.example`). It is not committed.

2. Start Minikube, build the images with Docker and load them into Minikube:
```powershell
minikube start
docker build -t api-gateway:1.0 ./api-gateway
docker build -t registration-service:1.0 ./registration-service
docker build -t update-service:1.0 ./update-service
minikube image load api-gateway:1.0
minikube image load registration-service:1.0
minikube image load update-service:1.0
```

3. Create the MongoDB secret and deploy:
```powershell
kubectl create secret generic mongodb-secret --from-env-file=.env
kubectl apply -f k8s/pods.yaml
kubectl apply -f k8s/services.yaml
kubectl get pods
kubectl get services
```

4. Access the API Gateway via Kubernetes NodePort (no port forwarding):
```powershell
minikube service student-gateway-service --url
```
This prints the active external URL routed directly to the `student-gateway-service` NodePort (port 30090), e.g. `http://127.0.0.1:64893`.

5. Import `postman/Student_Management_System.postman_collection.json` into Postman. Set the `base_url` variable to your Minikube service URL (or test directly with `http://127.0.0.1:64893`). Run the requests top to bottom: **Register Student** automatically saves the generated `Student_id`, and subsequent **Update** requests utilize it.

## Run locally without Kubernetes

```powershell
# each in its own terminal, with MONGODB_URI set
cd registration-service; npm install; npm start   # :5001
cd update-service;       npm install; npm start   # :5002
cd api-gateway;          npm install; $env:PORT=9090; npm start
```
