# SecureDrop
 - Secured way of Simple File sharing - 
# #
# Create the directory and environment
mkdir -p /opt/securedrop
cd /opt/securedrop
# #
# Install and activate VENV
python3 -m venv .venv
source .venv/bin/activate
# #
# Install required packages
# Upgrade pip first (recommended)
pip install --upgrade pip
# #
# Inside requirements.txt
fastapi
uvicorn
sqlalchemy
python-jose
passlib[bcrypti]
bcrypt==4.0.1
python-multipart
python-dotenv
email-validator
jinja2
alembic
# #
# Install a packages as per requirements
pip install -r requirements.txt
# #
# Now ready to start the SecureDrop app
chmod +x /opt/securedrop/securedrop.sh
./securedrop.sh start
# #
# Check the status
./securedrop.sh status
Running (PID xxxxxx)
# #
# Cross check
lsof -i tcp:8080
COMMAND    PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
uvicorn xxxxxx root    7u  IPv4 9108216      0t0  TCP *:http-alt (LISTEN)
# #
tail -f /var/log/securedrop.log
