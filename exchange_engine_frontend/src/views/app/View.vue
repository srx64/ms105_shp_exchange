<template>
  <v-app
    
  >
    <AppBar/>

    <v-main>
      <v-fade-transition mode="out-in">
        <router-view/>
      </v-fade-transition>
    </v-main>

    <BaseSnackbar
      dark
    />
  </v-app>
</template>

<script>
  export default {
    name: 'AppView',

    components: {
			AppBar: () => import('@/components/app/AppBar')
		},

    props: {
      id: {
        type: String,
        default: 'view',
      },
    },

    data: () => ({
      sections: [],
    }),

    methods: {
      showSnackbar () {
        this.$store.commit({
          type: 'showSnackbar',
          text: 'Hello'
        })
      }
    },

    onIdle () {
      console.log('refresh')
      this.$store.dispatch('userRefresh')
    }
  }
</script>