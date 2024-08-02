#!/bin/sh
#nohup hypercorn -b 127.0.0.1:8099 cdiapi.app:app&
hypercorn -b 127.0.0.1:8199 cdiapi.app:app > logs/api-int.log 2>&1 &