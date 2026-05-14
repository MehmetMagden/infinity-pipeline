# Infinity-Pipeline: SwissTask

A local Kubernetes infrastructure with automated CI/CD, monitoring, and secure external access.

## Project Overview
This project manages a Flask-based microservice (SwissTask) within a local Kubernetes cluster. It uses Infrastructure as Code (IaC) to handle everything from virtual machine provisioning to application deployment and observability.

## Architecture
The system runs on a 4-node cluster (1 Master, 3 Workers) virtualized via Vagrant and VirtualBox.

* **Infrastructure:** Provisioned using Ansible playbooks.
* **Orkestration:** Kubernetes (v1.28+) on Ubuntu 22.04 LTS.
* **Backend:** Flask API (Python 3.11) with PostgreSQL 15.
* **Network:** Flannel CNI for internal pod networking and Cloudflare Tunnels for secure HTTPS access.
* **Observability:** Prometheus and Grafana for system metrics.

## Tech Stack
- **Languages:** Python, SQL, YAML, Jinja2
- **Tools:** Kubernetes, Docker, Ansible, Vagrant, Helm
- **CI/CD:** GitHub Actions
- **Security:** Cloudflare Zero Trust (Tunnels), Kubernetes Secrets

## Pipeline Workflow
The "Infinity Pipeline" is defined in `.github/workflows/docker.yml`:
1. **QA:** Runs unit tests via `pytest` using an in-memory database.
2. **Build:** Containers are built and tagged with `GITHUB_SHA` for immutability.
3. **Registry:** Images are pushed to Docker Hub.
4. **Deploy:** Kubernetes updates the deployment using the specific commit-hash tag to ensure version consistency.

## Monitoring
The "Radar" system is accessible via `radar.aimaden.com`.
- **Prometheus:** Collects node and container metrics.
- **Grafana:** Visualizes resource usage (CPU, RAM, Network).

## The Battle Logs (Issues Resolved)
Practical challenges encountered and fixed during the build:
* **Swap Issues:** Kubernetes stability was achieved by disabling Linux Swap permanently across all nodes via Ansible.
* **Image Tagging:** Moved away from `:latest` tags to `GIT_SHA` to prevent pod synchronization errors and facilitate reliable rollbacks.
* **Dockerfile Optimization:** Fixed a 500 error by ensuring HTML templates and static files were explicitly copied into the multi-stage build.
* **Host Synchronization:** Resolved network desync caused by Windows host updates by implementing a systematic `vagrant reload` and K8s self-healing.

## Directory Structure
```text
.
├── ansible/          # Cluster provisioning and k8s setup
├── swisstask/
│   ├── app/          # Flask source code & Dockerfile
│   ├── k8s/          # Kubernetes manifests (Deployments, Secrets, Tunnels)
│   └── tests/        # Pytest suites
└── .github/          # CI/CD workflow definitions



How to Deploy
Provision VMs: vagrant up

Configure Cluster: ansible-playbook -i ansible/inventory.ini ansible/playbooks/01_base_setup.yml (and subsequent playbooks).

Apply Manifests: kubectl apply -f swisstask/k8s/