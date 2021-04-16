<template>
  <v-app
    @keyup.enter="snackbar = !snackbar"
  >
		<v-main
      class="pa-5"
    >
      <v-row
        justify="center"
      >
        <v-col
          cols="4"
        >
          <v-fade-transition mode="out-in">
            <router-view/>
          </v-fade-transition>
        </v-col>
      </v-row>
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

    props: {
      id: {
        type: String,
        default: 'view',
      },
    },

    data: () => ({
      sections: [],
    }),
  }
</script>