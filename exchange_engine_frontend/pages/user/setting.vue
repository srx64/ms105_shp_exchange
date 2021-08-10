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
        console.log(info)
      } catch {
        console.log('error')
      }
    }
  }
}
</script>

<style>

</style>
