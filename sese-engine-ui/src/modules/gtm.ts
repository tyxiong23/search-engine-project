import { createGtm } from '@gtm-support/vue-gtm'
import type { UserModule } from '~/types'

export const install: UserModule = ({ app }) => {
  // add google tag manager, and add GA4 in gtag
  app.use(createGtm({ id: 'GTM-PFF9NPT' }))
}
