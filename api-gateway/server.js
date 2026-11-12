// API Gateway - every request from Postman goes through here
// Pod 1: API Gateway + Registration Service (same pod -> localhost)
// Pod 2: Update Service (reached through the "update-service" Kubernetes Service)
const express = require('express');
const httpProxy = require('http-proxy');

const app = express();
const proxy = httpProxy.createProxyServer();

const PORT = process.env.PORT || 8080;
const REGISTRATION_SERVICE_URL = process.env.REGISTRATION_SERVICE_URL || 'http://localhost:5001';
const UPDATE_SERVICE_URL = process.env.UPDATE_SERVICE_URL || 'http://localhost:5002';

// NOTE: no body parser here, so the request body is streamed to the microservice unchanged

app.get('/', (req, res) => {
  res.json({
    service: 'API Gateway - Student Management System',
    routes: {
      'POST  /api/register': 'Registration Service (Pod 1)',
      'GET   /api/students': 'Registration Service (Pod 1)',
      'GET   /api/students/:id': 'Registration Service (Pod 1)',
      'PUT   /api/update/mobile/:id': 'Update Service (Pod 2)',
      'PUT   /api/update/password/:id': 'Update Service (Pod 2)',
      'PATCH /api/update/:id': 'Update Service (Pod 2)'
    }
  });
});

app.get('/health', (req, res) => {
  res.json({ service: 'api-gateway', status: 'UP' });
});

// Express strips the mount path from req.url, so put the full path back before forwarding
function forward(target, name) {
  return (req, res) => {
    console.log(`API GATEWAY -> ${name}: ${req.method} ${req.originalUrl}`);
    req.url = req.originalUrl;
    proxy.web(req, res, { target });
  };
}

app.use('/api/register', forward(REGISTRATION_SERVICE_URL, 'REGISTRATION SERVICE'));
app.use('/api/students', forward(REGISTRATION_SERVICE_URL, 'REGISTRATION SERVICE'));
app.use('/api/update', forward(UPDATE_SERVICE_URL, 'UPDATE SERVICE'));

proxy.on('error', (err, req, res) => {
  console.error('API Gateway proxy error:', err.message);
  if (!res.headersSent) {
    res.writeHead(502, { 'Content-Type': 'application/json' });
  }
  res.end(JSON.stringify({ error: 'Microservice unavailable', details: err.message }));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`API Gateway running on port ${PORT}`);
  console.log(`  /api/register, /api/students -> ${REGISTRATION_SERVICE_URL}`);
  console.log(`  /api/update                  -> ${UPDATE_SERVICE_URL}`);
});
