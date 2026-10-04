const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const pkg = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
for (const input of ['App.js', 'index.js', 'app.json', 'metro.config.js']) {
  if (!fs.existsSync(path.join(root, input))) throw new Error(`Missing app source: ${input}`);
}
if (!pkg.dependencies.expo || !pkg.dependencies['react-native']) throw new Error('Real dependencies missing');
const output = path.join(root, 'work');
fs.mkdirSync(output, {recursive: true});
fs.writeFileSync(path.join(output, 'qa-script-result.txt'), 'RN_SCRIPT_OK\n');
console.log('RN_SCRIPT_OK');
