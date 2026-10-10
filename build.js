const esbuild = require('esbuild');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 1. Roda o TypeScript
execSync('npm run tsc', { stdio: 'inherit' });

// 2. Copia a pasta config (se existir)
function copyRecursiveSync(src, dest) {
    if (!fs.existsSync(src)) return;
    if (fs.statSync(src).isDirectory()) {
        if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
        fs.readdirSync(src).forEach((childItemName) => {
            copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
        });
    } else {
        fs.copyFileSync(src, dest);
    }
}
copyRecursiveSync('config', 'dist/config');

// 3. Executa o esbuild
esbuild.build({
    entryPoints: ['./tsc-out/index.js'],
    bundle: true,
    sourcemap: process.env.NODE_ENV === 'development',
    platform: 'node',
    target: 'node26',
    outdir: 'dist',
    external: ['sharp'],
}).then(() => {
    // 4. Apaga a pasta temporária tsc-out após o sucesso
    if (fs.existsSync('tsc-out')) {
        fs.rmSync('tsc-out', { recursive: true, force: true });
    }
}).catch(() => process.exit(1));