<template>
  <section id="hero">
    <v-img
      :src="require('@/assets/light.jpg')"
      height="100vh"
      class="white--text"
      gradient="to bottom, rgba(11, 28, 61, .9), rgba(0,0,0,.4)"
    >  
      <v-container class="fill-height px-6 py-12">
        <v-responsive
          class="d-flex align-center mx-auto"
          height="100%"
          max-width="700"
          width="100%"
        >
          <BaseTitle
            weight="regular"
          >
            МЫ ХОТИМ СДЕЛАТЬ ПОКУПКУ АКЦИИ ПРОСТОЙ И ВЫГОДНОЙ
          </BaseTitle>          

          <BaseHeading
            size="text-h5"
            weight="medium"
          >
            ДОБРО ПОЖАЛОВАТЬ НА БИРЖУ EXCHANGE ENGINE
          </BaseHeading>

          <BaseBody>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Repudiandae nobis neque aspernatur in quas iure id aliquid, esse debitis, quibusdam mollitia! Quia ea expedita magnam totam, earum omnis et perspiciatis?
          </BaseBody>

          <div
            class="align-center d-flex flex-wrap"
          >
            <BaseBtn
              href="#features"
              x-large
            >
              Узнайте больше
            </BaseBtn>

            <span class="font-weight-bold ml-6 mr-4 my-4">или</span>

            <BaseBtn
              to="auth/reg"
              class="pa-1"
              height="auto"
              x-large
              text  
            >
              Начните сейчас
            </BaseBtn>
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
