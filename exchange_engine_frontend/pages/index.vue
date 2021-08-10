<template>
  <v-main>
    <section class="ex-section justify-center align-center">
      <div>
        <div class="display-4" style="font-family: 'Quantico', sans-serif !important;">
          SHP.EXchange
        </div>
        <v-row class="mt-8 justify-center">
          <v-col cols="auto">
            <v-btn color="primary" elevation="0" outlined to="/login">
              Войти
            </v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn color="primary" elevation="0" to="/register">
              Зарегистрироваться
            </v-btn>
          </v-col>
        </v-row>
      </div>
    </section>
    <section class="ex-section">
      <div class="display-4" style="font-family: 'Quantico', sans-serif !important;">
        SHP.EXchange
      </div>
    </section>
  </v-main>
</template>

<script>
export default {

}

</script>

<style>
  .ex-section {
    display: flex;
    min-height: 100vh;
    width: 100%;
  }

</style>
