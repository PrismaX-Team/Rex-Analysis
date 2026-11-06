import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

// BASE is the URL prefix the site is served under. Local and :8090 use "/"; GitHub Pages
// project sites live under "/<repo>/" and the workflow sets BASE for that build.
const base = process.env.BASE || "/";

export default defineConfig({
  base,
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@content": fileURLToPath(new URL("../content", import.meta.url)),
    },
  },
  server: {
    host: "127.0.0.1",
    port: 8090,
    allowedHosts: true,
    hmr: false,
  },
});
