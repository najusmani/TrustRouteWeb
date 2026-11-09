// Local preview of the website with GitHub-Pages-style clean URLs (/about -> about.html).
// Usage:  node tools/serve.mjs   then open http://localhost:8080
import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { join, extname, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../site/', import.meta.url));
const port = Number(process.env.PORT || 8080);
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.png': 'image/png', '.ico': 'image/x-icon',
};

async function resolve(urlPath) {
  const clean = normalize(decodeURIComponent(urlPath.split('?')[0])).replace(/^(\.\.[/\\])+/, '');
  const isDir = clean.endsWith('/') || clean.endsWith('\\');
  // like GitHub Pages: /page -> page.html, /folder -> folder/index.html
  const candidates = isDir
    ? [join(root, clean, 'index.html')]
    : [join(root, clean), join(root, clean + '.html'), join(root, clean, 'index.html')];
  for (const file of candidates) {
    if (!file.startsWith(root)) continue;
    try { if ((await stat(file)).isFile()) return file; } catch { /* try next */ }
  }
  return null;
}

http.createServer(async (req, res) => {
  const file = await resolve(req.url || '/');
  if (!file) { res.writeHead(404, { 'Content-Type': 'text/plain' }); return res.end('Not found'); }
  res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
  res.end(await readFile(file));
}).listen(port, '127.0.0.1', () => console.log(`Previewing site/ at http://localhost:${port}`));
