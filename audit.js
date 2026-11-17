const fs=require('fs');const h=fs.readFileSync('site/index.html','utf8');const s=h.split('<script>')[1].split('</script>')[0];
const pre=s.split('let active=null;')[0];eval(pre.replace(/const /g,'var '));
const issues=[];
const gidToM={oot:'oot',albw:'albw',tfh:'tfh',botw:'botw',sky_ss:null,sky_totk:null};
GAMES.forEach(g=>{const mid=g.id;const m=M[mid];
 if(!m){issues.push(`card ${mid}: no table column`);return}
 g.mk.forEach(k=>{if(!AREAS[k[0]])issues.push(`${mid}: unknown area ${k[0]}`);if(!m[k[0]])issues.push(`${mid}: marker "${k[3]}" (${k[0]}) but table says absent`)});
 if(!fs.existsSync('site/maps/'+g.img))issues.push(`${mid}: missing image ${g.img}`);
 (g.v||[]).concat(g.extra||[]).forEach(v=>{if(!fs.existsSync('site/maps/'+v[0]))issues.push(`${mid}: missing ${v[0]}`)});
 const dup={};g.mk.forEach(k=>{const key=k[1]+','+k[2];if(dup[key])issues.push(`${mid}: overlapping markers ${dup[key]} / ${k[3]}`);dup[key]=k[3]});
});
Object.keys(M).forEach(k=>{if(!GAMES.find(g=>g.id===k))issues.push(`table column ${k}: no map card`)});
REFS.forEach(r=>{if(r[6]){const all=GAMES.concat(SKY);const g=all.find(x=>x.id===r[6][0]);if(!g)issues.push(`ref ${r[1]}: origin game ${r[6][0]} missing`);else if(!g.mk.find(m=>m[0]===r[6][1]))issues.push(`ref ${r[1]}: no ${r[6][1]} marker on ${r[6][0]}`)}});
console.log(issues.join('\n')||'no issues');
let bytes=0;fs.readdirSync('site/maps').forEach(f=>bytes+=fs.statSync('site/maps/'+f).size);console.log('images MB',(bytes/1e6).toFixed(1));
