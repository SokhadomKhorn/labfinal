# Student Management System - Microservices, Docker & Kubernetes

**Student:** Khorn Sokhadom  
**2nd microservice:** Update student mobile number or password

## Architecture

```
Postman ──► api-gateway-service (NodePort 30080)
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
k8s/services.yaml       api-gateway-service (NodePort) + update-service (ClusterIP)
k8s/secret.example.yaml MongoDB secret template
postman/                Postman collection
```

## Run on Minikube

1. Put your MongoDB connection string in a `.env` file in the project root (see `.env.example`). It is not committed.

2. Start Minikube and build the images inside it:
```powershell
minikube start
minikube image build -t api-gateway:1.0 ./api-gateway
minikube image build -t registration-service:1.0 ./registration-service
minikube image build -t update-service:1.0 ./update-service
```

3. Create the MongoDB secret and deploy:
```powershell
kubectl create secret generic mongodb-secret --from-env-file=.env
kubectl apply -f k8s/pods.yaml
kubectl apply -f k8s/services.yaml
kubectl get pods
kubectl get services
```

4. Open the gateway for Postman:
```powershell
kubectl port-forward service/api-gateway-service 9090:8080
```

5. Import `postman/Student_Management_System.postman_collection.json` into Postman and run the requests top to bottom. **Register Student** saves the new `Student_id`, and the **Update** requests use it.

## Run locally without Kubernetes

```powershell
# each in its own terminal, with MONGODB_URI set
cd registration-service; npm install; npm start   # :5001
cd update-service;       npm install; npm start   # :5002
cd api-gateway;          npm install; $env:PORT=9090; npm start
```
