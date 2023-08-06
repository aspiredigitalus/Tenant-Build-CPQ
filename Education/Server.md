# Aspire Digital Server
---
## Contents

[1. Hosting](#1-Hosting)  
[2. Databases](#2-Databases)  
[3. Website](#3-Website)  
[4. CI/CD](#4-CICD)  
[5. SonarQube](#5-SonarQube)  
[6. Useful CentOS Linux Commands](#6-Useful-CentOS-Linux-Commands)  

### 1. Hosting
    - Login: https://162.240.108.85:2087
    - UI Interface: CPanel
    - OS: CentOS 7.9

### 2. Databases

#### 2.1 MySQL

#### 2.2 Postgres

### 3. Website

    - Front End: Angular 4
        - HTML, CSS, Typescript
    - API: Sprint Boot
        - JAVA

### 4. CI/CD

#### 4.1 Repository
    cd ~/git/aspiredigital

#### 4.2 Shell Scripts
    /usr/bin/sh /home/aspiredigital/cronjob/deploy.sh

#### 4.3 Cron Job
    - Minute    0
    - Hour	    0,12
    - Day	    *
    - Month	    *
    - Weekday   *

### 5. SonarQube

#### 5.1 Saved Settings On Reboot of Server
```
sudo nano /etc/sysctl.conf

vm.max_map_count=524288
fs.file-max=131072

sudo nano /etc/security/limits.conf

ulimit -n 131072
ulimit -u 8192
```

### 6. Useful CentOS Linux Commands

#### 6.1 OS Commands
Exit VI editor
```
[ESC] -> [SHIFT]: -> wq
```

Access Sudoers File
```
sudo visudo
```
Add user to the Wheel Group (root group)
```
sudo usermod -aG wheel <username>
```

Rebooting Full System  
    It is best to shut down Databases first
```
sudo sync;sync
sudo systemctl stop postgresql-15
sudo systemctl stop mysql # MySQL/MariDB -> command not working
sudo systemctl reboot
```

#### 6.2 Postgres Commands
Start the Database
```
sudo systemctl start postgresql-15
```

Enable on Reboot
```
sudo systemctl enable postgresql-15
```

Restart the Database
```
sudo service postgresql-15 restart
```

Get Status of Current Server
```
sudo service postgresql-15 status
```

Get .conf location as Linux user
```
sudo -u postgres psql -c 'SHOW config_file'
```

Get .conf location as postgres user
```
psql -U postgres -c 'SHOW config_file'
```

Get pg_hba.conf location as Linux user
```
sudo -u postgres psql -t -P format=unaligned -c 'show hba_file';
```

#### 6.3 Docker Commands
Pull new SonarQube docker image
```
docker pull sonarqube
```

Create new container for SonarQube
```
sudo docker run -d --name sonarqube \
-p 9000:9000 \
-e SONAR_JDBC_URL=jdbc:postgresql://localhost/sonarqube \
-e SONAR_JDBC_USERNAME=sonarqube \
-e SONAR_JDBC_PASSWORD=<password> \
-v sonarqube_data:/opt/sonarqube/data \
-v sonarqube_extensions:/opt/sonarqube/extensions \
-v sonarqube_logs:/opt/sonarqube/logs \
sonarqube
```

Show all containers
```
sudo docker container ls -a
```

Delete Container
```
sudo docker stop <container id>
sudo docker rm <container id>
```
Make container restart automatically
```
sudo docker update --restart <command> <container id>
```
```
Commands:
no	Do not automatically restart the container. (the default)

on-failure[:max-retries]	Restart the container if it exits due to an error, 
    which manifests as a non-zero exit code. Optionally, limit the number of 
    times the Docker daemon attempts to restart the container using the :max-retries option.

always	Always restart the container if it stops. If it is manually stopped, 
    it is restarted only when Docker daemon restarts or the container itself 
    is manually restarted. (See the second bullet listed in restart policy details)

unless-stopped	Similar to always, except that when the container is stopped 
    (manually or otherwise), it is not restarted even after Docker daemon restarts.
```

Get Docker Host IP
```
sudo ip -4 addr show docker0
```