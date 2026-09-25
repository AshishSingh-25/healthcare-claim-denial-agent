import test from 'node:test';
import assert from 'node:assert/strict';
import handler from '../api/[...path].js';

function setOrigin(t,value) {
  const previous=process.env.CLAIM_API_ORIGIN;
  process.env.CLAIM_API_ORIGIN=value;
  t.after(()=>{if(previous===undefined) delete process.env.CLAIM_API_ORIGIN; else process.env.CLAIM_API_ORIGIN=previous;});
}
function response() {return {code:200,headers:{},setHeader(k,v){this.headers[k]=v},status(n){this.code=n;return this},json(payload){this.payload=payload;return this}}}
test('forwards a sample claim to the configured HTTPS backend',async t=>{
  setOrigin(t,' https://claims-api.droidrex.me\n');
  const data={claim_id:'CLM001'};
  t.mock.method(globalThis,'fetch',async (url,options)=>{
    assert.equal(url.href,'https://claims-api.droidrex.me/api/assess');
    assert.equal(options.body,JSON.stringify(data));
    return new Response(JSON.stringify({analysis:'Sample analysis'}),{headers:{'Content-Type':'application/json'}});
  });
  const res=response(); await handler({url:'/api/assess',method:'POST',body:data},res);
  assert.equal(res.code,200); assert.equal(res.payload.analysis,'Sample analysis');
});
test('returns a readable error when the upstream firewall returns HTML',async t=>{
  setOrigin(t,'https://claims-api.droidrex.me');
  t.mock.method(globalThis,'fetch',async ()=>new Response('<html>Blocked</html>',{status:403,headers:{'Content-Type':'text/html'}}));
  t.mock.method(console,'error',()=>{});
  const res=response(); await handler({url:'/api/health',method:'GET'},res);
  assert.equal(res.code,503); assert.match(res.payload.detail,/temporarily unavailable/);
});
test('rejects unknown routes and unsupported methods without contacting the backend',async t=>{
  t.mock.method(globalThis,'fetch',()=>{throw new Error('must not fetch')});
  for(const [url,method,status] of [['/api/unknown','GET',404],['/api/assess','DELETE',405]]){
    const res=response(); await handler({url,method},res); assert.equal(res.code,status);
  }
});
