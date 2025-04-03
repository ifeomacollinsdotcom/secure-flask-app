server {
  listen 80;
  server_name {{ domain_name }};

  location / {
      proxy_pass http://localhost:5000;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;