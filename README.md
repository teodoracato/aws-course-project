# AWS course project

A small Python (Flask) project used throughout the AWS course.

## Structure

```
common/            shared code (used by more than one artifact)
  ec2_metadata.py  reads region / AZ / instance id from the EC2 metadata service
webapp/            artifact 1: web application
  app.py           endpoints: /  /api/info  /health
  requirements.txt Python packages the app needs
build.sh           builds dist/webapp.tar.gz (Linux, GitHub Actions)
build.ps1          builds dist/webapp.tar.gz on Windows, -Upload sends it to S3
.github/workflows/ automatic build on every push to main
```

## Build

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1          # build only
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Upload  # build + upload to S3
```

Linux / CI:

```bash
bash build.sh
```

## Run on a server

```bash
tar -xzf webapp.tar.gz -C /opt/webapp
cd /opt/webapp
pip3 install -r requirements.txt
gunicorn --bind 0.0.0.0:80 webapp.app:app
```
