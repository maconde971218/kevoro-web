import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { writeFile, symlink, unlink } from "node:fs/promises";

test("preview serves public pages and rejects repository internals and traversal", async () => {
  const server = spawn(process.execPath, [
    "scripts/preview.mjs",
    "--port",
    "8876",
  ]);
  try {
    await writeFile(".preview-private-fixture", "synthetic test fixture");
    await symlink("../.preview-private-fixture", "assets/preview-test-link");
    await once(server.stdout, "data");
    const base = "http://127.0.0.1:8876";
    for (const path of ["/", "/marca/", "/assets/app.js"]) {
      const response = await fetch(base + path);
      assert.equal(response.status, 200, path);
      assert.equal(response.headers.get("x-content-type-options"), "nosniff");
    }
    for (const path of [
      "/assets/preview-test-link",
      "/.git/config",
      "/.agents/skills/frontend-design/SKILL.md",
      "/assets/%2e%2e%2f.git/config",
      "/package.json",
      "/assets/%5c..%5c.git/config",
    ]) {
      assert.equal((await fetch(base + path)).status, 404, path);
    }
  } finally {
    server.kill("SIGTERM");
    await once(server, "exit");
    await unlink("assets/preview-test-link");
    await unlink(".preview-private-fixture");
  }
});
