#!/bin/bash
#Kill the existing process
pkill -9 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8080 >> /var/log/secure-file-share.log 2>&1 &
