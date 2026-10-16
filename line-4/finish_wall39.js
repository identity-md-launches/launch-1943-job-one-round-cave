// One-time export: retain generated pigment only; never redraw ancestor marks.
'use strict';
const fs = require('node:fs'), zlib = require('node:zlib'), crypto = require('node:crypto');
const {decode, thumbnail} = require('../gathering/thumbnail.js');
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const beforeBytes = fs.readFileSync('artifacts/line-4/wall-v18.png');
const candidateBytes = fs.readFileSync('artifacts/line-4/wall-v19.png');
if (hash(beforeBytes) !== '7b39817bfde4e32831af7a877cb564dc40ed2ecd63058e4df4641a83072c672a') throw Error('wrong ancestor');
const old = decode(beforeBytes), candidate = decode(candidateBytes);
if (old.width !== 1254 || old.height !== 1254 || candidate.width !== 1254 || candidate.height !== 1254) throw Error('wrong dimensions');
if (hash(candidateBytes) !== 'fe07e0d9b57bce2a5be235bc7ace7379eabed6273b71feb775c73d0d04f63f9c') throw Error('expected original generated candidate; finished output is not a candidate');
// Reviewed six pebble silhouettes and three crooked paths in the generated edit.
const nodes = [[804,214],[831,224],[855,230],[817,271],[842,282],[879,286]];
const trails = [[[804,221],[806,241],[814,250],[817,263]],
                [[831,232],[833,246],[840,259],[842,274]],
                [[855,238],[861,247],[871,261],[879,278]]];
function segmentDistance(x,y,a,b) {
  const dx=b[0]-a[0],dy=b[1]-a[1];
  const t=Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));
  return Math.hypot(x-a[0]-t*dx,y-a[1]-t*dy);
}
function inMotif(x,y) {
  if(nodes.some(([nx,ny])=>Math.hypot(x-nx,y-ny)<=12))return true;
  return trails.some(points=>points.slice(1).some((point,i)=>segmentDistance(x,y,points[i],point)<4));
}
const pixels=Buffer.from(old.pixels), left=990, top=185, sx=790,sy=200,width=104,height=100;
let changed=0;
for(let y=0;y<height;y++)for(let x=0;x<width;x++) {
  const gx=sx+x,gy=sy+y;
  if(!inMotif(gx,gy))continue;
  const p=(gy*candidate.width+gx)*candidate.channels;
  const [r,g,b]=candidate.pixels.subarray(p,p+3);
  // Extract charcoal/ochre coverage rather than copying generated rock.
  if(r>145 || g>100 || b>76)continue;
  const red=r>g*1.4 && r>70;
  const a=Math.min(0.88,Math.max(0,(red?150-g:130-r)/110));
  if(a<0.15)continue;
  const pigment=red?[139,54,26]:[47,34,24];
  const dest=((top+y)*old.width+left+x)*old.channels;
  for(let c=0;c<3;c++)pixels[dest+c]=Math.round(pixels[dest+c]*(1-a)+pigment[c]*a);
  changed++;
}
if(changed<700)throw Error('insufficient generated pigment');
function crc32(b){let c=0xffffffff;for(const v of b){c^=v;for(let i=0;i<8;i++)c=(c>>>1)^((c&1)?0xedb88320:0);}return(c^0xffffffff)>>>0;}
function chunk(n,b){const k=Buffer.from(n),s=Buffer.alloc(4),c=Buffer.alloc(4);s.writeUInt32BE(b.length);c.writeUInt32BE(crc32(Buffer.concat([k,b])));return Buffer.concat([s,k,b,c]);}
const header=Buffer.alloc(13);header.writeUInt32BE(old.width);header.writeUInt32BE(old.height,4);header[8]=8;header[9]=2;
const stride=old.width*3,scan=Buffer.alloc(old.height*(stride+1));
for(let y=0;y<old.height;y++)pixels.copy(scan,y*(stride+1)+1,y*stride,(y+1)*stride);
const png=Buffer.concat([Buffer.from('89504e470d0a1a0a','hex'),chunk('IHDR',header),chunk('IDAT',zlib.deflateSync(scan,{level:9})),chunk('IEND',Buffer.alloc(0))]);
const jpg=thumbnail(png,512,75);
if(jpg.length>100000)throw Error('preview too large');
let outside=0;
for(let y=0;y<old.height;y++)for(let x=0;x<old.width;x++) {
  if(x>=left && x<left+width && y>=top && y<top+height)continue;
  const p=(y*old.width+x)*3;
  if(!pixels.subarray(p,p+3).equals(old.pixels.subarray(p,p+3)))outside++;
}
if(outside)throw Error('ancestor pixels changed outside addition');
for(const name of ['wall-v19.png','wall.png'])fs.writeFileSync('artifacts/line-4/'+name,png);
fs.writeFileSync('dist/line-4/39.jpg',jpg);
const checks={ancestor_sha256:hash(beforeBytes),generated_candidate_sha256:hash(candidateBytes),
  method:'Built-in imagegen edit; extracted generated charcoal/ochre silhouette and placed it on bare rock. Candidate consumed in place.',
  source_crop:[sx,sy,sx+width-1,sy+height-1],
  png:{paths:['artifacts/line-4/wall-v19.png','artifacts/line-4/wall.png'],format:'PNG',mode:'RGB',dimensions:[old.width,old.height],bytes:png.length,sha256:hash(png)},
  jpeg:{path:'dist/line-4/39.jpg',format:'JPEG',dimensions:[512,512],bytes:jpg.length,sha256:hash(jpg)},
  preservation:{rectangle:[left,top,left+width-1,top+height-1],changed_pixels:changed,outside_rectangle_changed_pixels:outside},
  visual_review_completed:false,unmet_visual_requirements:[]};
fs.writeFileSync('line-4/image-checks39.json',JSON.stringify(checks,null,2)+'\n');
console.log(JSON.stringify(checks,null,2));
