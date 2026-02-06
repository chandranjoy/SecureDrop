# SecureDrop - Secured way of Simple File sharing
# #
# Create the directory and environment
- mkdir -p /opt/securedrop
- cd /opt/securedrop
# #
# Install and activate VENV
- python3 -m venv .venv
- source .venv/bin/activate
# #
# Install required packages
# Upgrade pip first (recommended)
- pip install --upgrade pip
# #
# Inside requirements.txt
- cat requirements.txt
_fastapi
uvicorn
sqlalchemy
python-jose
passlib[bcrypti]
bcrypt==4.0.1
python-multipart
python-dotenv
email-validator
jinja2
alembic_
# #
# Install a packages as per requirements
- pip install -r requirements.txt
# #
# Now ready to start the SecureDrop app
- chmod +x /opt/securedrop/securedrop.sh
- ./securedrop.sh start
# #
# Check the status
- ./securedrop.sh status
_Running (PID xxxxxx)_
# #
# Cross check
- lsof -i tcp:8080
COMMAND    PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
uvicorn xxxxxx root    7u  IPv4 9108216      0t0  TCP *:http-alt (LISTEN)
# #
- tail -f /var/log/securedrop.log
_INFO:     10.255.254.10:57590 - "GET /admin/login HTTP/1.1" 200 OK
INFO:     10.255.254.10:39868 - "POST /admin/login HTTP/1.1" 302 Found
INFO:     10.255.254.10:39868 - "GET /admin/dashboard HTTP/1.1" 200 OK
INFO:     10.255.254.10:55988 - "GET /download/5 HTTP/1.1" 200 OK
INFO:     10.255.254.10:46774 - "POST /download/5 HTTP/1.1" 303 See Other
INFO:     10.255.254.10:46774 - "GET /download/5/success HTTP/1.1" 200 OK
INFO:     10.255.254.10:46774 - "GET /download/5/file HTTP/1.1" 200 OK
INFO:     10.255.254.10:56564 - "GET /download/ HTTP/1.1" 404 Not Found
INFO:     10.255.254.10:43744 - "GET /admin/logout HTTP/1.1" 302 Found
INFO:     10.255.254.10:43744 - "GET /admin/login HTTP/1.1" 200 OK_
