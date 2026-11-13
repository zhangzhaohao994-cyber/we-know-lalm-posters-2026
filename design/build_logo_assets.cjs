const fs=require('fs'),path=require('path'),sharp=require('sharp');
const dir=path.join(__dirname,'../assets/logo-composites');
(async()=>{for(const n of fs.readdirSync(dir).filter(n=>n.endsWith('.svg'))){await sharp(path.join(dir,n)).png().toFile(path.join(dir,n.replace('.svg','.png')));}console.log('Rendered reusable transparent logo composites');})().catch(e=>{console.error(e);process.exit(1)});
