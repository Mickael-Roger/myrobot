[Unit]
Description=${ROBOT_SVC} service
After=rabbitmq-server.service

[Service]
Type=simple
Environment=PYTHONUNBUFFERED=1
Environment=RABBITMQ_DEFAULT_USER='robot'
Environment=RABBITMQ_DEFAULT_PASS='2a55f70a841f18b97c3a7db939b7adc9e34a0f1b'
ExecStart=/usr/bin/python3 /app/${ROBOT_SVC}.py
User=root
Restart=on-failure
StandardOutput=file:/var/log/${ROBOT_SVC}

[Install]
WantedBy=multi-user.target
