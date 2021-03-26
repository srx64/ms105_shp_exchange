import Vue from 'vue'
import VueMeta from 'vue-meta'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './router'
import './plugins/base'

Vue.use(VueMeta)

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
