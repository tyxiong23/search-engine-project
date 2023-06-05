// import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// import App from './App.vue'
import type { UserModule } from '~/types'

export const install: UserModule = ({ app }) => {
    app.use(ElementPlus)
}
