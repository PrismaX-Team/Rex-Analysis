// GitHub Pages has no rewrite rules: an unknown path such as /afe/1.0/tasks/x returns 404.html.
// Copying index.html to 404.html makes that page boot the app, and the router then renders the
// requested route. Run after `vite build`.
import { copyFileSync } from "node:fs";
copyFileSync("dist/index.html", "dist/404.html");
console.log("dist/404.html written");
