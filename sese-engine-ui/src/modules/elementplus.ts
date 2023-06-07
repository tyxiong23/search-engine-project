// import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// import App from './App.vue'
import type { UserModule } from '~/types'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

export const install: UserModule = ({ app }) => {
    app.use(ElementPlus)
    for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
        app.component(key, component)
    }
}
