const http = require('http');
const httpProxy = require('http-proxy');

// Create a proxy server
const proxy = httpProxy.createProxyServer({});

// Define the target backend server
const target = 'http://localhost:8001'; // Change this to your backend server

// Create an HTTP server
const server = http.createServer((req, res) => {
  // Forward the request to the backend server
  proxy.web(req, res, { target: target }, (error) => {
    console.error('Proxy error:', error);
    res.writeHead(502, { 'Content-Type': 'text/plain' });
    res.end('Bad Gateway');
  });
});

// Start the server
const PORT = 8000;
server.listen(PORT, () => {
  console.log(`Reverse proxy server is running on port ${PORT}`);
});
