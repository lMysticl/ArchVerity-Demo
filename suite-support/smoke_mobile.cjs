// Observe actual Metro and Expo loopback servers and stop only our child trees.
const {spawn, execFileSync} = require('node:child_process');
const http = require('node:http');
const net = require('node:net');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../projects/mobile-lab');

async function freePort() {
  const server = net.createServer();
  await new Promise((resolve, reject) => server.once('error', reject).listen(0, '127.0.0.1', resolve));
  const port = server.address().port;
  await new Promise(resolve => server.close(resolve));
  return port;
}

function status(port) {
  return new Promise((resolve, reject) => {
    const request = http.get(`http://127.0.0.1:${port}/status`, response => {
      let body = '';
      response.on('data', chunk => { body += chunk; });
      response.on('end', () => resolve({status: response.statusCode, body}));
    });
    request.setTimeout(1000, () => request.destroy(new Error('timeout')));
    request.once('error', reject);
  });
}

async function run(mode) {
  const port = await freePort();
  const script = require.resolve(mode === 'metro' ? 'react-native/cli.js' : 'expo/bin/cli', {paths: [root]});
  const args = mode === 'metro' ? ['start', '--port', String(port)] : ['start', '--localhost', '--port', String(port)];
  const directory = path.join(root, 'work');
  fs.mkdirSync(directory, {recursive: true});
  const fd = fs.openSync(path.join(directory, `${mode}-smoke.log`), 'w');
  const processHandle = spawn(process.execPath, [script, ...args], {
    cwd: root, stdio: ['ignore', fd, fd], windowsHide: true, detached: process.platform !== 'win32',
    env: {...process.env, CI: '1', EXPO_NO_TELEMETRY: '1', EXPO_OFFLINE: '1'},
  });
  fs.closeSync(fd);
  const exited = new Promise(resolve => processHandle.once('exit', resolve));
  let observed;
  try {
    const deadline = Date.now() + 45000;
    while (Date.now() < deadline) {
      if (processHandle.exitCode !== null) throw new Error(`${mode} exited early: ${processHandle.exitCode}`);
      try {
        observed = await status(port);
        if (observed.status === 200 && observed.body === 'packager-status:running') break;
      } catch {}
      await new Promise(resolve => setTimeout(resolve, 250));
    }
    if (!observed || observed.body !== 'packager-status:running') throw new Error(`${mode} did not become ready`);
  } finally {
    if (processHandle.exitCode === null) {
      if (process.platform === 'win32') {
        try {
          execFileSync('taskkill.exe', ['/PID', String(processHandle.pid), '/T', '/F'], {stdio: 'ignore', windowsHide: true});
        } catch {
          // taskkill may race with exit; exit/closed-port proof decides the result.
        }
      } else {
        process.kill(-processHandle.pid, 'SIGTERM');
      }
    }
    await Promise.race([exited, new Promise((_, reject) => setTimeout(() => reject(new Error(`${mode} child did not exit`)), 5000))]);
  }
  let stopped = false;
  try { await status(port); } catch { stopped = true; }
  if (!stopped) throw new Error(`${mode} still answers after child shutdown`);
  return {mode, port, status: observed.body, childStopped: stopped};
}

(async () => {
  const observations = [];
  for (const mode of ['metro', 'expo']) observations.push(await run(mode));
  const receipt = {status: 'LOCAL_DEV_SERVERS_PASS', observations, boundary: 'Actual CLI/server processes; separate from IDEA buttons/native device run'};
  fs.writeFileSync(path.join(root, 'work/mobile-smoke.json'), JSON.stringify(receipt, null, 2));
  console.log(JSON.stringify(receipt));
})().catch(error => { console.error(error.message); process.exitCode = 1; });
