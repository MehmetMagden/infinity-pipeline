# Infinity-Pipeline: SwissTask

A local Kubernetes infrastructure running an automated CI/CD pipeline and a Python microservice.

## Project Overview
This project manages a Flask-based microservice (SwissTask) within a local Kubernetes cluster. It uses Infrastructure as Code (IaC) to handle everything from virtual machine provisioning to application deployment and observability.

## Architecture Overview
The environment is built on four virtual machines (1 Master, 3 Workers) managed via Vagrant and VirtualBox on a local network (`192.168.56.x`).

* **Operating System:** Ubuntu 22.04 LTS
* **Container Runtime:** Containerd
* **Orchestration:** Kubernetes v1.28
* **Networking:** Flannel CNI, Cloudflare Tunnels
* **Monitoring:** Prometheus, Grafana

## Tech Stack
- **Languages:** Python, SQL, YAML, Jinja2
- **Tools:** Kubernetes, Docker, Ansible, Vagrant, Helm
- **CI/CD:** GitHub Actions
- **Security:** Cloudflare Zero Trust (Tunnels), Kubernetes Secrets

## Infrastructure Automation (Ansible)
The cluster is provisioned from scratch using Ansible. The playbooks in `ansible/playbooks/` are executed sequentially to ensure a stable environment:

* `01_base_setup.yml`: Installs base dependencies, configures kernel modules (`overlay`, `br_netfilter`), and disables swap memory.
* `01_2_hostname_fix.yml`: Assigns correct hostnames (`k8s-master`, `k8s-worker1`, etc.) based on IP addresses.
* `01_5_network_fix.yml`: Configures IPv4 forwarding and sysctl parameters required for Kubernetes networking.
* `01_8_containerd_fix.yml`: Installs and configures Containerd with `SystemdCgroup=true`.
* `02_install_k8s.yml`: Installs `kubelet`, `kubeadm`, and `kubectl` on all nodes.
* `03_master_init.yml`: Initializes the Kubernetes control plane using `kubeadm` and applies the Flannel network plugin.
* `04_workers_join.yml`: Fetches the join token from the master and automatically connects worker nodes to the cluster.
* `05_deploy_swisstask.yml`: Applies the application manifests (API, Database, Tunnels) to the cluster.
* `06_deploy_monitoring.yml`: Installs Prometheus and Grafana using Helm charts for system observability.

## Application Architecture
The backend is a task management API named SwissTask.

* **Framework:** Python 3.11 with Flask.
* **Database:** PostgreSQL 15-Alpine, deployed as a stateful pod in the cluster.
* **Security:** Database credentials are managed via Kubernetes Secrets (`db-secret`) and passed as environment variables.
* **Containerization:** Built using a multi-stage Dockerfile. The application runs as a non-root user (`swisstaskuser`) for security.

## Kubernetes Resources
The `swisstask/k8s/` directory defines the cluster state:

* `swisstask-deployment.yaml`: Manages the API with 3 replicas for high availability and rolling updates.
* `swisstask-db.yaml`: Manages the PostgreSQL database deployment and its internal service.
* `swisstask-secret.yaml`: Stores base64-encoded credentials.
* `swisstask-service.yaml`: Exposes the API internally to the cluster via a LoadBalancer/ClusterIP.
* `cloudflare-tunnel.yaml`: Deploys a `cloudflared` pod to route external traffic securely to the local cluster without opening router ports.

## CI/CD Pipeline
The automated workflow is defined in `.github/workflows/docker.yml` and triggers on pushes to the `main` branch.

1. **Test Stage:** Sets up Python, installs dependencies, and runs the `pytest` suite using an in-memory SQLite database to verify code integrity.
2. **Build Stage:** Builds the Docker image and pushes it to Docker Hub.
3. **Tagging Strategy:** Images are tagged with the specific Git commit SHA (`GITHUB_SHA`) instead of `:latest`. This ensures immutable deployments and reliable rollbacks in Kubernetes.

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
├── ansible
│   ├── inventory.ini
│   └── playbooks
│       ├── 01_2_hostname_fix.yml
│       ├── 01_5_network_fix.yml
│       ├── 01_8_containerd_fix.yml
│       ├── 01_base_setup.yml
│       ├── 02_install_k8s.yml
│       ├── 03_master_init.yml
│       ├── 04_workers_join.yml
│       ├── 05_deploy_swisstask.yml
│       └── 06_deploy_monitoring.yml
└── swisstask
    ├── app
    │   ├── app.py
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── templates
    │       └── index.html
    ├── k8s
    │   ├── cloudflare-tunnel.yaml
    │   ├── swisstask-db.yaml
    │   ├── swisstask-deployment.yaml
    │   ├── swisstask-secret.yaml
    │   └── swisstask-service.yaml
    └── tests
        ├── __init__.py
        └── test_app.py

7 directories, 21 files