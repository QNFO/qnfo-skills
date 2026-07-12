// qwav-unified — merged deep-qwav-meta + qwav-redirect
// Session 13 — 2026-07-11
// Routes: deep.qwav.tech/* → proxy with meta | qwav.tech/* → 301 redirect

var ORIGIN = "https://qwav.pages.dev";

var OG_TAGS = `
<meta property="og:title" content="QWAV Deep — Research Feed">
<meta property="og:description" content="QNFO research feed on ultrametric quantum computing, p-adic physics, and quantum foundations. Browse papers with DOIs and AI-powered Q&A.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://deep.qwav.tech/">
<meta property="og:site_name" content="QWAV Deep">
<meta property="og:image" content="https://qnfo.org/favicon.ico">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="QWAV Deep — Research Feed">
<meta name="twitter:description" content="Browse QNFO research papers with AI-powered Q&A.">
`;

var JSON_LD = `
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "QWAV Deep",
  "url": "https://deep.qwav.tech/",
  "description": "QNFO research feed on ultrametric quantum computing, p-adic physics, and quantum foundations.",
  "publisher": {
    "@type": "Organization",
    "name": "QNFO",
    "url": "https://qnfo.org"
  }
}
</script>
`;

async function proxyWithMeta(request) {
  const url = new URL(request.url);
  const targetUrl = ORIGIN + url.pathname + url.search;
  
  try {
    const upstream = await fetch(targetUrl, {
      headers: request.headers,
      method: request.method,
      redirect: "manual",
    });
    
    const contentType = upstream.headers.get("Content-Type") || "";
    
    if (contentType.includes("text/html")) {
      let html = await upstream.text();
      // Inject OG tags before </head>
      html = html.replace("</head>", OG_TAGS + JSON_LD + "</head>");
      
      return new Response(html, {
        status: upstream.status,
        headers: {
          "Content-Type": "text/html; charset=utf-8",
          "Cache-Control": "public, max-age=3600",
          "Access-Control-Allow-Origin": "*",
        }
      });
    }
    
    // Pass through non-HTML responses
    let headers = new Headers(upstream.headers);
    headers.set("Access-Control-Allow-Origin", "*");
    return new Response(upstream.body, {
      status: upstream.status,
      headers: headers,
    });
  } catch (e) {
    return new Response("Origin unreachable", { status: 502 });
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const hostname = url.hostname;
    
    // qwav.tech / www.qwav.tech → 301 redirect to deep.qwav.tech
    if (hostname === "qwav.tech" || hostname === "www.qwav.tech") {
      const targetUrl = "https://deep.qwav.tech" + url.pathname + url.search;
      return Response.redirect(targetUrl, 301);
    }
    
    // deep.qwav.tech → proxy to Pages with meta injection
    if (hostname === "deep.qwav.tech") {
      return proxyWithMeta(request);
    }
    
    // Fallback: proxy with meta
    return proxyWithMeta(request);
  }
};
