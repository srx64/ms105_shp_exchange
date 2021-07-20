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
            МЫ ХОТИМ НАУЧИТЬ ПОКУПАТЬ АКЦИИ ПРОСТО И ЛЕГКО
          </BaseTitle>          

          <BaseHeading
            size="text-h5"
            weight="medium"
          >
            ДОБРО ПОЖАЛОВАТЬ НА БИРЖУ ШКОЛЫ ПРОГРАММИСТОВ
          </BaseHeading>

          <BaseBody>
            Данный проект позволит вам научиться основам финансирования, 
            наглядно и просто научит базовым приёмам, необходимым для умения 
            грамотно приобретать акции, распоряжаться ими для своей выгоды.
          </BaseBody>

          <div
            class="align-center d-flex flex-wrap"
          >
            <BaseBtn
              @click="$vuetify.goTo('#features', {duration: 300, offset: -10, easing: 'easeInOutCubic'})"
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
