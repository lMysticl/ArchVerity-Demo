const fs = require('node:fs');
const path = require('node:path');

const output = path.join(__dirname, '..', 'work', 'qa-script-result.txt');
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, 'RN_SCRIPT_OK\n', 'utf8');
process.stdout.write(`RN_SCRIPT_OK ${output}\n`);
