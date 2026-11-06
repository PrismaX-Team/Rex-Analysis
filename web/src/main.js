import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router";
import "@fontsource/space-grotesk/400.css";
import "@fontsource/space-grotesk/600.css";
import "@fontsource/jetbrains-mono/400.css";
import "./styles/main.scss";
import "./styles/home.scss";
import "./styles/board.scss";
import "./styles/hub.scss";

createApp(App).use(router).mount("#app");
