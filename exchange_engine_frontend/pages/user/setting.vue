<template>
  <v-main>
    <v-container>
      <v-row class="pt-5 justify-center">
        <v-col cols="12">
          <h1>Настройки</h1>
          <FormDefSetting :submit-form="submit" />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  components: {
    FormDefSetting: () => import('@/components/form/setting.vue')
  },
  layout: 'app',
  methods: {
    submit (info) {
      try {
        this.$axios.patch('api/v1/profile/', {
          first_name: info.first_name,
          last_name: info.last_name,
          email: info.email
        })
      } catch {
        console.log('error')
      }
    }
  }
}
</script>

<style>

</style>
