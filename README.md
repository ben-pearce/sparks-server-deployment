# 🤖 Development Server Deployment

This repository contains my Docker Compose files and configuration files for services hosted on my development workstation/server. The goal is to create a remote development environment accessible via a thin client from anywhere, leveraging additional computing power and eliminating the need to maintain multiple instances of my environments.

## Containers

| **Name** | **Description** | **Ports** | **Links** |
|---|---|---|---|
| [portainer-agent](./docker-compose.monitoring.yml#L5)  | Portainer edge agent. |  | [GitHub](https://github.com/portainer/agent) |
| [zabbix-agent](./docker-compose.monitoring.yml#L21)  | Zabbix agent for monitoring. |  | [Docker Hub](https://hub.docker.com/r/zabbix/zabbix-agent) |
| [traefik](./docker-compose.yml#L10)  |  | `0.0.0.0:80:80`, `0.0.0.0:443:443` |  |
| [code-server](./stacks/docker-compose.code.yml#L5)  | VS Code in the browser |  | [GitHub](https://github.com/coder/code-server) |
| [barbie-github-runner](./stacks/docker-compose.github.yml#L5)  |  |  |  |
| [etch-github-runner](./stacks/docker-compose.github.yml#L21)  |  |  |  |
| [jessie-github-runner](./stacks/docker-compose.github.yml#L37)  |  |  |  |
| [rc-github-runner](./stacks/docker-compose.github.yml#L53)  |  |  |  |
| [sparks-github-runner](./stacks/docker-compose.github.yml#L69)  |  |  |  |
| [woody-github-runner](./stacks/docker-compose.github.yml#L87)  |  |  |  |
| [zurg-github-runner](./stacks/docker-compose.github.yml#L103)  |  |  |  |
| [syncthing](./stacks/docker-compose.syncthing.yml#L5)  | Free and open source peer-to-peer file synchronization | `0.0.0.0:21027:21027/udp`, `0.0.0.0:22000:22000/tcp`, `0.0.0.0:22000:22000/udp` | [Website](https://syncthing.net/) |



## Prerequisites

A linux-based operating system with [docker](https://docs.docker.com/engine/install/) installed.

## Configuration
The `.env` file stores environment variables to make starting the containers easy. This should be modified to match your needs before starting the containers for the first time.

| **Variable** | **Description** | **Example** |
|---|---|---|
| `HOST` | The main host for web-based services. | `sparks` |
| `SMTP_HOST` | SMTP mail server host. | `mail.example.com` |
| `SMTP_USER` | SMTP username. | `postmaster@example.com` |
| `TZ` | Timezone for all containers. | `Europe/London` |
| `PUID` | System user ID to run containers as. | `1000` |
| `PGID` | System group ID to run containers as. | `1000` |
| `CONFIG_DIR` | Location of config storage on host. | `config` |
| `DATA_DIR` | Location of data storage on host. | `data` |
| `ADMIN_EMAIL` | Administrative email address. | `somebody@example.com` |
| `AUTHELIA_HOST` | Remote Authelia host. | `login.example.com` |
| `HOST_IP` | IP Address of the host. | `172.0.0.1` |
| `NFS_HOST` | Host of NFS shares. | `nfs.example.com` |
| `ZBX_HOSTNAME` | Zabbix server hostname. | `zabbix-server` |
| `ZBX_SERVER_HOST` | Zabbix monitoring server host. | `zabbix.example.com` |
| `ZBX_REFRESHACTIVECHECKS` | Zabbix active check interval. | `60` |


## Contributions

First of all, **thanks for your interest!** But due to this being a personal project of mine tailored to my own needs, I cannot accept pull requests on this repository. Please feel free to fork and tweak this project though.