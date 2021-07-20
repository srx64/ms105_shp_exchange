<template>
  <v-row class="justify-center">
    <v-col cols="8">
      <h1>Настройки</h1>
      <h5 class="mt-5 text-h6">
        Основная информация
      </h5>
      <v-form v-model="valid">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field v-model="firstname" :rules="nameRules" :counter="10" label="First name" required />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field v-model="lastname" :rules="nameRules" :counter="10" label="Last name" required />
          </v-col>
          <v-col cols="12">
            <v-text-field v-model="lastname" :rules="nameRules" :counter="10" label="Last name" required />
          </v-col>
          <v-col cols="12">
            <v-text-field v-model="lastname" :rules="nameRules" :counter="10" label="Last name" required />
          </v-col>
        </v-row>
        <v-btn color="primary">
          Validate
        </v-btn>
      </v-form>
      <h5 class="mt-10 text-h6">
        Смена пароля
      </h5>
      <v-form v-model="valid">
        <v-row>
          <v-col cols="12">
            <v-text-field v-model="lastname" :rules="nameRules" :counter="10" label="Last name" required />
          </v-col>
          <v-col cols="12">
            <v-text-field v-model="lastname" :rules="nameRules" :counter="10" label="Last name" required />
          </v-col>
        </v-row>
        <v-btn color="primary">
          Validate
        </v-btn>
      </v-form>
    </v-col>
  </v-row>
</template>

<script>
export default {
}
</script>

<style>

</style>
