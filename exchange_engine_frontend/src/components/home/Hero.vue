<template>
  <section id="hero">
    <v-img
      :src="require('@/assets/light.jpg')"
      height="100vh"
      class="white--text"
      gradient="to bottom, rgba(11, 28, 61, .9), rgba(0,0,0,.4)"
    >  
      <v-container class="fill-height px-4 py-12">
        <v-responsive
          class="d-flex align-center mx-auto"
          height="100%"
          max-width="700"
          width="100%"
        >
          <h5
            class="font-weight-regular mb-2 text-left"
            style="font-size: 1rem; letter-spacing: 0.24rem"
          >
            МЫ ХОТИМ СДЕЛАТЬ ПОКУПКУ АКЦИИ ПРОСТОЙ И ВЫГОДНОЙ
          </h5>

          <h2
            class="font-weight-medium mb-4 text-left"
            style="font-size: 1.65rem"
          >
            ДОБРО ПОЖАЛОВАТЬ НА БИРЖУ EXCHANGE ENGINE
          </h2>

          <p
            class="grey--text mb-6"
          >
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Repudiandae nobis neque aspernatur in quas iure id aliquid, esse debitis, quibusdam mollitia! Quia ea expedita magnam totam, earum omnis et perspiciatis?
          </p>

          <div
            class="align-center d-flex flex-wrap"
          >
            <v-tooltip left>
              <template v-slot:activator="{ on, attrs }">
                <div
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-btn
                    color="primary"
                    disabled
                    depressed
                    x-large
                    tile
                  >
                    Узнайте больше
                  </v-btn>
                </div>
              </template>
              <span>Извините, раздел в разработке</span>
            </v-tooltip>

            <span class="font-weight-bold ml-6 mr-4 my-4">или</span>

            <v-btn
              to="auth/registration"
              color="primary"
              class="pa-1 font-weight-bold"
              height="auto"
              min-width="164"
              depressed
              x-large
              text
              tile
            >
              Начните сейчас
            </v-btn>
          </div>
        </v-responsive>
      </v-container>
    </v-img>
  </section>
</template>

<script>
  export default {
    name: 'Hero',
  }
</script>
