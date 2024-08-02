#!/bin/sh
#nohup hypercorn -b 127.0.0.1:8099 cdiapi.app:app&
#set CDI_MEILISEARCH_KEY='d8f91c1d4999a23810d0c0fad095508c4d4a36902fceb98eb43c1bea6221e1b3'
hypercorn -b 127.0.0.1:8099 cdiapi.app:app