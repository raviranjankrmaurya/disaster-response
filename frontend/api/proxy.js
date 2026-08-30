export default async function handler(req, res) {
  const backendUrl = process.env.BACKEND_URL;
  const apiKey = process.env.API_KEY;

  if (!backendUrl || !apiKey) {
    return res.status(500).json({
      detail: "Vercel environment variables are missing"
    });
  }

  const path = req.query.path || "";

  const targetUrl = `${backendUrl}/api/${path}`;

  try {
    const headers = {
      "X-API-Key": apiKey,
      "Content-Type": "application/json",
    };

    const options = {
      method: req.method,
      headers,
    };

    if (!["GET", "HEAD"].includes(req.method)) {
      options.body =
        typeof req.body === "string"
          ? req.body
          : JSON.stringify(req.body);
    }

    const response = await fetch(targetUrl, options);
    const text = await response.text();

    res.status(response.status);

    const contentType = response.headers.get("content-type");
    if (contentType) {
      res.setHeader("Content-Type", contentType);
    }

    return res.send(text);
  } catch (error) {
    console.error("Proxy error:", error);

    return res.status(502).json({
      detail: "Backend unavailable"
    });
  }
}
