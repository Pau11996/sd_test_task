# My Weather Project

## Description
Service for getting weather from 3rd API, caching in Redis, loging results in DynamoDB, upload JSON file in Minio (S3)

This application is designed to perform a test task, in the production version it is subject to revision 
(creation of .env, clearer separation into layers)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Pau11996/sd_test_task.git
   cd sd_test_task
   docker compose build
   docker compose up
   curl http://127.0.0.1:5000/api/v1/weather?city=London
   
Check ports if it's needed