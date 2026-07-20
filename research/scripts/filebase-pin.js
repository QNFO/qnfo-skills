#!/usr/bin/env node
// filebase-pin.js — Pin a file to IPFS via Filebase (S3-compatible, auto-pins on PUT)
// PRIMARY IPFS pinner as of 2026-07-20 (replaces Pinata, whose free quota was exceeded).
// Free tier: 5GB storage, no request-volume rate limit.
// Usage: node filebase-pin.js <file-path> <bucket> [key]
// Requires: FILEBASE_ACCESS_KEY, FILEBASE_SECRET_KEY env vars (or ~/.filebase_access_key, ~/.filebase_secret_key)
//
// RED-TEAM FIX (2026-07-20, verified live): Filebase does NOT return an
// x-ipfs-cid header on the PUT response — that header does not exist on PUT
// at all. Pinning is ASYNCHRONOUS. The real CID only appears later via a
// HEAD request, in the x-amz-meta-cid header, once x-amz-meta-pinning-status
// reaches "pinned" (observed latency ~5-10s live). This script now PUTs,
// then polls HEAD until the CID appears (or times out).

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const AK = process.env.FILEBASE_ACCESS_KEY;
const SK = process.env.FILEBASE_SECRET_KEY;
const HOST = 's3.filebase.com';

function hmac(key, data) {
  return crypto.createHmac('sha256', key).update(data).digest();
}

function contentTypeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const map = {
    '.md': 'text/markdown',
    '.pdf': 'application/pdf',
    '.zip': 'application/zip',
    '.json': 'application/json',
    '.txt': 'text/plain',
    '.html': 'text/html',
  };
  return map[ext] || 'application/octet-stream';
}

function sigV4Headers(method, objPath, contentType, payloadHash) {
  const amzDate = new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
  const dateStamp = amzDate.substring(0, 8);

  const signedHeadersList = contentType
    ? 'content-type;host;x-amz-content-sha256;x-amz-date'
    : 'host;x-amz-content-sha256;x-amz-date';

  const canonicalReq = [
    method, objPath, '',
    ...(contentType ? ['content-type:' + contentType] : []),
    'host:' + HOST,
    'x-amz-content-sha256:' + payloadHash,
    'x-amz-date:' + amzDate + '\n',
    signedHeadersList,
    payloadHash
  ].join('\n');

  const credentialScope = dateStamp + '/us-east-1/s3/aws4_request';
  const stringToSign = [
    'AWS4-HMAC-SHA256', amzDate, credentialScope,
    crypto.createHash('sha256').update(canonicalReq).digest('hex')
  ].join('\n');

  const kDate = hmac('AWS4' + SK, dateStamp);
  const kRegion = hmac(kDate, 'us-east-1');
  const kService = hmac(kRegion, 's3');
  const kSigning = hmac(kService, 'aws4_request');
  const signature = hmac(kSigning, stringToSign).toString('hex');

  const auth = 'AWS4-HMAC-SHA256 Credential=' + AK + '/' + credentialScope +
    ',SignedHeaders=' + signedHeadersList + ',Signature=' + signature;

  const headers = { Authorization: auth, Host: HOST, 'x-amz-content-sha256': payloadHash, 'x-amz-date': amzDate };
  if (contentType) headers['Content-Type'] = contentType;
  return headers;
}

async function s3Put(bucket, key, body, contentType) {
  const payloadHash = crypto.createHash('sha256').update(body).digest('hex');
  const objPath = '/' + bucket + '/' + key;
  const headers = sigV4Headers('PUT', objPath, contentType, payloadHash);
  const r = await fetch('https://' + HOST + objPath, { method: 'PUT', headers, body });
  return { status: r.status, ok: r.ok };
}

async function s3Head(bucket, key) {
  const objPath = '/' + bucket + '/' + key;
  const payloadHash = crypto.createHash('sha256').update('').digest('hex');
  const headers = sigV4Headers('HEAD', objPath, null, payloadHash);
  const r = await fetch('https://' + HOST + objPath, { method: 'HEAD', headers });
  return {
    status: r.status,
    ok: r.ok,
    ipfsCid: r.headers.get('x-amz-meta-cid'),
    pinningStatus: r.headers.get('x-amz-meta-pinning-status')
  };
}

async function filebasePin(filePath, bucket, key, maxAttempts = 6, delayMs = 3000) {
  if (!AK || !SK) throw new Error('FILEBASE_ACCESS_KEY / FILEBASE_SECRET_KEY not set');
  const content = fs.readFileSync(filePath);
  const objectKey = key || path.basename(filePath);
  const contentType = contentTypeFor(filePath);

  const putResult = await s3Put(bucket, objectKey, content, contentType);
  if (!putResult.ok) {
    console.error('Filebase upload FAILED: HTTP', putResult.status);
    console.error('Falling back: try scripts/lighthouse-pin.js next. Do NOT retry Pinata (quota exceeded, blocked).');
    process.exitCode = 1;
    return null;
  }
  console.log('Filebase upload: HTTP', putResult.status, '(pinning is async — polling for CID...)');

  for (let i = 0; i < maxAttempts; i++) {
    await new Promise(res => setTimeout(res, delayMs));
    const head = await s3Head(bucket, objectKey);
    if (head.ipfsCid) {
      console.log('IPFS CID:', head.ipfsCid, '(pinning-status:', head.pinningStatus + ')');
      console.log('Gateway (ipfs.io):', 'https://ipfs.io/ipfs/' + head.ipfsCid);
      console.log('Gateway (dweb.link):', 'https://dweb.link/ipfs/' + head.ipfsCid);
      return head.ipfsCid;
    }
  }
  console.error('WARNING: CID not available after', maxAttempts * delayMs / 1000, 'seconds.');
  console.error('The object uploaded successfully but Filebase has not finished pinning yet.');
  console.error('Re-run a HEAD check later, or increase maxAttempts.');
  process.exitCode = 1;
  return null;
}

if (require.main === module) {
  const [filePath, bucket, key] = process.argv.slice(2);
  if (!filePath || !bucket) {
    console.error('Usage: node filebase-pin.js <file-path> <bucket> [key]');
    process.exit(1);
  }
  filebasePin(filePath, bucket, key).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { filebasePin, s3Put, s3Head };
