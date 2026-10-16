// Reverse proxy local HTTP -> https://www.helloharel.com, pour que Chromium
// (qui ne lit pas la CA du proxy d'agent) puisse capturer le site reel.
// Tout le TLS sortant est verifie par Node contre /root/.ccr/ca-bundle.crt.
import http from 'node:http';

const UP = 'https://www.helloharel.com';
const PORT = Number(process.env.MIRROR_PORT || 8099);
const LOCAL = `http://127.0.0.1:${PORT}`;
const TEXT = /^(text\/|application\/(javascript|json|xml|xhtml|rss|ld\+json)|image\/svg)/;

function rewrite(s) {
  return s
    .split('https://www.helloharel.com').join(LOCAL)
    .split('https:\\/\\/www.helloharel.com').join(LOCAL.replace(/\//g, '\\/'))
    .split('http://www.helloharel.com').join(LOCAL)
    .split('//www.helloharel.com').join(`//127.0.0.1:${PORT}`)
    .split('https://helloharel.com').join(LOCAL);
}

http.createServer(async (req, res) => {
  const url = UP + req.url;
  try {
    const up = await fetch(url, {
      headers: {
        'user-agent': req.headers['user-agent'] || 'Mozilla/5.0',
        'accept': req.headers.accept || '*/*',
        'accept-language': 'fr-FR,fr;q=0.9',
      },
      redirect: 'follow',
    });
    const ct = up.headers.get('content-type') || 'application/octet-stream';
    const headers = { 'content-type': ct, 'cache-control': 'no-store', 'access-control-allow-origin': '*' };
    if (TEXT.test(ct)) {
      res.writeHead(up.status, headers);
      res.end(rewrite(await up.text()));
    } else {
      const buf = Buffer.from(await up.arrayBuffer());
      res.writeHead(up.status, headers);
      res.end(buf);
    }
  } catch (e) {
    res.writeHead(502, { 'content-type': 'text/plain' });
    res.end('mirror error: ' + e.message);
  }
}).listen(PORT, '127.0.0.1', () => console.log('mirror up on ' + LOCAL));
