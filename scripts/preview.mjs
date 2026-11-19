import { createServer } from "node:http";
import { readFile, realpath, stat } from "node:fs/promises";
import { resolve, extname, sep, relative } from "node:path";
import { fileURLToPath } from "node:url";
const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const index = process.argv.indexOf("--port");
const port = Number(
  index >= 0 ? process.argv[index + 1] : process.env.PORT || 3000,
);
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css",
  ".js": "text/javascript",
  ".mjs": "text/javascript",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
  ".png": "image/png",
  ".json": "application/json",
  ".md": "text/plain; charset=utf-8",
  ".txt": "text/plain",
  ".xml": "application/xml",
};
function isPublic(path) {
  const parts = path.split("/").filter(Boolean);
  return (
    !parts.some((part) => part.startsWith(".") || part.includes("\\")) &&
    (!parts.length ||
      [
        "index.html",
        "assets",
        "marca",
        "instagram",
        "robots.txt",
        "sitemap.xml",
      ].includes(parts[0]))
  );
}
// Solo archivos públicos: nunca sirve .git, skills ni configuración privada.
createServer(async (req, res) => {
  try {
    const pathname = decodeURIComponent(
      new URL(req.url, "http://localhost").pathname,
    );
    if (!isPublic(pathname)) throw Error("Not public");
    let path = resolve(root, "." + pathname);
    if ((await stat(path)).isDirectory()) path = resolve(path, "index.html");
    path = await realpath(path);
    if (
      !path.startsWith(root + sep) ||
      !isPublic(relative(root, path).split(sep).join("/"))
    )
      throw Error("Outside public root");
    const data = await readFile(path);
    res.writeHead(200, {
      "Content-Type": types[extname(path)] || "application/octet-stream",
      "X-Content-Type-Options": "nosniff",
      "Cache-Control": "no-store",
    });
    res.end(req.method === "HEAD" ? undefined : data);
  } catch {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("No encontrado");
  }
}).listen(port, "127.0.0.1", () =>
  console.log(`Kevoro preview: http://localhost:${port}`),
);
