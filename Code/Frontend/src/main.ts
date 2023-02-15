import { createApp } from "vue"
import router from "./router"
import App from "./App.vue"
import axios from 'axios'
import VueAxios from 'vue-axios'
import ElementPlus from "element-plus";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'


const app = createApp(App).use(router)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

app.use(VueAxios, axios)
app.use(ElementPlus)

app.mount("#app")
app.config.globalProperties.$axios = axios;
