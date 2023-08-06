# Aspire Digital Server
---
## Contents

[1. Hosting](#1-Hosting)  
[2. Databases](#2-Databases)  
[3. Website](#3-Website)  
[4. CI/CD](#4-CI-CD)

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

