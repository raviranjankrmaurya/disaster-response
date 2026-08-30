export default async function handler(req, res) {
  const backendUrl = process.env.BACKEND_URL;
  const apiKey = process.env.API_KEY;

  if (!backendUrl || !apiKey) {
    return res.status(500).json({
      detail: "Server configuration missing"
    });
  }

  const path = Array.isArray(req.query.path)
    ? req.query.path.join("/")
    : req.query.path || "";

  const query = new URLSearchParams(req.query);
  query.delete("path");

  const targetUrl =
    `${backendUrl}/api/${path}` +
    (query.toString() ? `?${query.toString()}` : "");

  const headers = {
    "Content-Type": "application/json",
    "X-API-Key": apiKey,
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

  try {
    const response = await fetch(targetUrl, options);
    const text = await response.text();

    res.status(response.status);

    const contentType = response.headers.get("content-type");

    if (contentType) {
      res.setHeader("Content-Type", contentType);
    }

    return res.send(text);
  } catch (error) {
    console.error(error);

    return res.status(502).json({
      detail: "Backend unavailable"
    });
  }
}
