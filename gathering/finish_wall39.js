// Isolate the new pigment from the image tool's output onto the verified wall.
// Usage: node gathering/finish_wall39.js GENERATED_PNG
'use strict';
const fs = require('node:fs');
const zlib = require('node:zlib');
const crypto = require('node:crypto');
const {decode, thumbnail} = require('./thumbnail.js');

const ancestorBytes = fs.readFileSync('artifacts/gathering/wall-v18.png');
const ancestorHash = '00ef58619cf56be7e4f8289561dfd73194c91f2d37b4d4caccf171ca3de14382';
if (crypto.createHash('sha256').update(ancestorBytes).digest('hex') !== ancestorHash)
  throw new Error('expected the verified Gathering 38 ancestor');
const freshBytes = fs.readFileSync(process.argv[2]);
if(crypto.createHash('sha256').update(freshBytes).digest('hex')!=='a3b71359d8c1f9aaaa497f8710f5c9901c46cc2c940d5dc5d449edbbd73ee08a') throw new Error('requires original image tool candidate, not finished wall');
const old = decode(ancestorBytes), fresh = decode(freshBytes);
if (old.width !== 1254 || old.height !== 1254 || old.channels !== 3 ||
    fresh.width !== old.width || fresh.height !== old.height || fresh.channels < 3)
  throw new Error('image dimensions or format changed');

// Transfer only the generated pigment silhouette onto a reviewed bare patch.
// The candidate moved the new motif over an ancestor handprint. Discard that
// repaint entirely: retain the ancestor everywhere and relocate only new marks.
const width=old.width,height=old.height;
const out=Buffer.from(old.pixels);
const box=[420,920,510,1005];
const circles=[[710,298,12],[772,326,12],[792,216,12],[820,271,12]];
const segments=[[[719,292],[757,263]],[[757,263],[783,223]],
                [[757,263],[809,270]],[[731,287],[764,317]]];
function nearSegment(x,y,a,b){
 const dx=b[0]-a[0],dy=b[1]-a[1];
 const t=Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)));
 return Math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)<5;
}
let changed=0,changedBox=[width,height,-1,-1];
for(let y=box[1];y<=box[3];y++)for(let x=box[0];x<=box[2];x++){
 const sx=Math.round((x-465)/.65+760),sy=Math.round((y-960)/.65+270);
 const circle=circles.some(([cx,cy,r])=>Math.hypot(sx-cx,sy-cy)<r);
 const line=segments.some(([a,b])=>nearSegment(sx,sy,a,b));
 if(!circle&&!line)continue;
 const q=(sy*width+sx)*fresh.channels,p=(y*width+x)*3;
 const [r,g,b]=fresh.pixels.subarray(q,q+3);
 const pigment=circle ? (r<120&&g<85&&b<60)||(r>g*1.4&&g>b*1.3)||(r>150&&g>125&&b>95) : r<110&&g<80&&b<55;
 if(!pigment)continue;
 for(let c=0;c<3;c++)out[p+c]=Math.round(old.pixels[p+c]*.12+fresh.pixels[q+c]*.88);
 if(out[p]!==old.pixels[p]||out[p+1]!==old.pixels[p+1]||out[p+2]!==old.pixels[p+2]){
  changed++;changedBox=[Math.min(changedBox[0],x),Math.min(changedBox[1],y),Math.max(changedBox[2],x),Math.max(changedBox[3],y)];
 }
}
if(changed<300||changed>3500)throw new Error('unexpected new pigment count '+changed);
function crc32(bytes) {
  let crc=0xffffffff;
  for(const v of bytes){crc^=v;for(let b=0;b<8;b++)crc=(crc>>>1)^((crc&1)?0xedb88320:0);}
  return (crc^0xffffffff)>>>0;
}
function chunk(name,data) {
  const kind=Buffer.from(name),length=Buffer.alloc(4),crc=Buffer.alloc(4);
  length.writeUInt32BE(data.length);crc.writeUInt32BE(crc32(Buffer.concat([kind,data])));
  return Buffer.concat([length,kind,data,crc]);
}
const ihdr=Buffer.alloc(13);
ihdr.writeUInt32BE(width);ihdr.writeUInt32BE(height,4);ihdr[8]=8;ihdr[9]=2;
const stride=width*3,scan=Buffer.alloc(height*(stride+1));
for(let y=0;y<height;y++)out.copy(scan,y*(stride+1)+1,y*stride,(y+1)*stride);
const png=Buffer.concat([Buffer.from('89504e470d0a1a0a','hex'),chunk('IHDR',ihdr),
  chunk('IDAT',zlib.deflateSync(scan,{level:9})),chunk('IEND',Buffer.alloc(0))]);
fs.writeFileSync('artifacts/gathering/wall-v19.png',png);
fs.writeFileSync('artifacts/gathering/wall.png',png);
const jpeg=thumbnail(png,512,75);
if(jpeg.length>=100000)throw new Error('JPEG exceeds 100 KB');
fs.writeFileSync('dist/gathering/39.jpg',jpeg);
const result={ancestor_sha256:ancestorHash,
  generated_sha256:crypto.createHash('sha256').update(freshBytes).digest('hex'),
  png:{path:'artifacts/gathering/wall-v19.png',format:'PNG',mode:'RGB',dimensions:[width,height],
    bytes:png.length,sha256:crypto.createHash('sha256').update(png).digest('hex')},
  jpeg:{path:'dist/gathering/39.jpg',format:'JPEG',dimensions:[512,512],bytes:jpeg.length},
  preservation:{rectangle:box,changed_pixels:changed,changed_bounds:changedBox,
                outside_rectangle_changed_pixels:0},
  model:'installed image edit tool; generated pigment isolated over verified ancestor',
  visual_review_completed:false,unmet_visual_requirements:[]};
fs.writeFileSync('gathering/image-checks39.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
