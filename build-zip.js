import { zip } from 'zip-a-folder';
import { mkdirSync } from 'fs';

async function main() {
    mkdirSync('./public', { recursive: true });
    await zip('./src', './public/src.zip');
    console.log('✅ Zipped src/ -> public/src.zip');
}

main();
