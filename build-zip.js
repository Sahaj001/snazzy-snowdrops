import { zip } from 'zip-a-folder';
import { mkdirSync } from 'fs';

async function main() {
    mkdirSync('./dist', { recursive: true });
    await zip('./src', './dist/src.zip');
    console.log('✅ Zipped src/ -> dist/src.zip');
}

main();
