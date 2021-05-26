<template>
  <v-app>
		<v-main
      class="pa-10"
    >
      <v-fade-transition mode="out-in">
        <router-view/>
      </v-fade-transition>
    </v-main>

    <BaseSnackbar
      align="center"
      dark
    />
  </v-app>
</template>

<script>
  export default {
    name: 'AuthView',

    metaInfo: {
      title: 'Авторизация',
    },

    props: {
      id: {
        type: String,
        default: 'view',
      },
    },
  }
</script>