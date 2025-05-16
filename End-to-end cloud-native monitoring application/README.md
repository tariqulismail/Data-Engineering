# 🚀 End-to-End Cloud-Native Monitoring Application on Kubernetes (AWS EKS)

This project demonstrates how to build and deploy a Python-based system monitoring application using **Flask**, **psutil**, **Docker**, **Amazon ECR**, and **Kubernetes (EKS)**. It covers everything from writing the monitoring logic to deploying a containerized app in a production-ready Kubernetes environment on AWS.

---

## 📌 Features

- ✅ System Resource Monitoring using `psutil`
- ✅ Flask-based Web API to serve metrics
- ✅ Dockerized application with custom `Dockerfile`
- ✅ Push image to AWS ECR using `boto3`
- ✅ Deploy container to AWS EKS with Kubernetes manifests
- ✅ Kubernetes Deployments and Services written in Python

---

## 🧠 Tech Stack

- **Python 3.10+**
- **Flask** – Micro web framework for Python
- **psutil** – System and process utilities
- **Docker** – Containerization platform
- **AWS ECR** – Elastic Container Registry for image storage
- **AWS EKS** – Managed Kubernetes Service
- **Kubernetes** – Container orchestration platform
- **Boto3** – AWS SDK for Python

---

## 🛠️ Project Structure

├── app/
│   ├── app.py               # Flask Monitoring App using psutil
│   └── requirements.txt     # Dependencies
├── docker/
│   └── Dockerfile           # Dockerfile for building the image
├── k8s/
│   ├── deployment.py        # Kubernetes Deployment via Python
│   └── service.py           # Kubernetes Service via Python
├── ecr/
│   └── push_to_ecr.py       # Script to push Docker image to ECR using Boto3
├── README.md

---

## 🚧 Step-by-Step Guide

### 1. 🔍 Monitoring Application with Flask & psutil

```bash
cd app/
pip install -r requirements.txt
python app.py

Access the monitoring app locally at http://localhost:5000/metrics.

2. 🐳 Dockerize the Application

cd docker/
docker build -t monitoring-app:latest .
docker run -p 5000:5000 monitoring-app


3. ☁️ Push Docker Image to AWS ECR
cd ecr/
python push_to_ecr.py

This script will:
	•	Authenticate Docker with ECR
	•	Create an ECR repository (if not existing)
	•	Tag and push the local Docker image

⸻

4. ☸️ Deploy to Kubernetes on AWS EKS
	1.	Create an EKS Cluster using AWS Console or CLI.
	2.	Configure kubectl to use your EKS cluster.
