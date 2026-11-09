const fs=require('fs'),path=require('path');
const sharp=require('sharp');
const root=path.resolve(__dirname,'..');
const full=process.argv.includes('--print'); const selected=process.argv.slice(2).filter(x=>!x.startsWith('--'));
(async()=>{for(const f of fs.readdirSync(path.join(root,'sources')).filter(x=>x.endsWith('.svg'))){
const id=f.slice(0,-4);if(selected.length&&!selected.includes(id))continue;let svg=fs.readFileSync(path.join(root,'sources',f),'utf8');
if(full){svg=svg.replace('width="1200" height="1800"','width="7087" height="10630"');await sharp(Buffer.from(svg),{limitInputPixels:false}).png({compressionLevel:9}).withMetadata({density:300}).toFile(path.join(root,'print',id+'.png'));}
else{await sharp(Buffer.from(svg),{limitInputPixels:false}).jpeg({quality:91,chromaSubsampling:'4:4:4'}).toFile(path.join(root,'previews',id+'.jpg'));}
console.log(id,full?'print':'preview');}})().catch(e=>{console.error(e);process.exit(1)});
