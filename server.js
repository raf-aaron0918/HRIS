const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const legacyRoot = path.join(__dirname, 'dist');
const vueRoot = path.join(__dirname, 'dist-vue');
const hasVueBuild = fs.existsSync(path.join(vueRoot, 'index.html'));
const root = hasVueBuild ? vueRoot : legacyRoot;
const host = process.env.HOST || '127.0.0.1';
const port = Number(process.env.PORT || 3000);
const shouldOpenBrowser = process.env.NO_OPEN !== '1' && process.env.CI !== 'true';

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.eot': 'application/vnd.ms-fontobject'
};

function send(res, code, body, type) {
  res.writeHead(code, { 'Content-Type': type || 'text/plain; charset=utf-8' });
  res.end(body);
}

function redirect(res, location) {
  res.writeHead(302, { Location: location });
  res.end();
}

function resolveFile(urlPath) {
  let cleanPath = decodeURIComponent(urlPath.split('?')[0]);
  if (cleanPath === '/') cleanPath = '/index.html';

  const withoutQuery = cleanPath.replace(/^\/+/, '');
  const candidateRoots = [];

  if (withoutQuery.startsWith('dist/')) {
    candidateRoots.push({
      base: __dirname,
      path: path.join(__dirname, withoutQuery),
      spaFallback: false,
    });
  } else {
    candidateRoots.push({
      base: root,
      path: path.join(root, withoutQuery),
      spaFallback: hasVueBuild,
    });
  }

  for (const candidate of candidateRoots) {
    const direct = candidate.path;

    if (fs.existsSync(direct) && fs.statSync(direct).isDirectory()) {
      return path.join(direct, 'index.html');
    }

    if (fs.existsSync(direct)) {
      return direct;
    }

    if (!path.extname(direct) && fs.existsSync(`${direct}.html`)) {
      return `${direct}.html`;
    }

    if (candidate.spaFallback && !path.extname(withoutQuery)) {
      return path.join(root, 'index.html');
    }
  }

  return null;
}

function openBrowser(url) {
  if (!shouldOpenBrowser) {
    return;
  }

  const opener =
    process.platform === 'win32'
      ? 'cmd'
      : process.platform === 'darwin'
        ? 'open'
        : 'xdg-open';

  const args = process.platform === 'win32' ? ['/c', 'start', '""', url] : [url];

  spawn(opener, args, {
    detached: true,
    stdio: 'ignore',
    shell: false,
  }).unref();
}

const server = http.createServer((req, res) => {
  const requestPath = decodeURIComponent((req.url || '/').split('?')[0]);
  if (requestPath === '/register' || requestPath === '/pages/register.html') {
    redirect(res, '/login');
    return;
  }
  const filePath = resolveFile(req.url || '/');
  if (!filePath) {
    send(res, 404, 'Not found');
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = mimeTypes[ext] || 'application/octet-stream';

  fs.createReadStream(filePath)
    .on('error', () => send(res, 500, 'Server error'))
    .once('open', () => {
      res.writeHead(200, { 'Content-Type': contentType });
    })
    .pipe(res);
});

server.listen(port, host, () => {
  const url = `http://${host}:${port}`;
  console.log(`Serving ${root} at ${url}`);
  openBrowser(url);
});

