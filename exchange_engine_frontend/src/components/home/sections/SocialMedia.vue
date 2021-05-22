<template>
  <v-theme-provider dark>
    <base-section
      id="social"
      class="blue darken-2 text-center"
      space="56"
    >
      <base-icon class="mb-8">
        mdi-telegram
      </base-icon>

      <base-section-heading
        color="transparent"
        title="Наш Telegram"
      >
        Следите за новостями и обновлениями на нашем канале Telegram
      </base-section-heading>

      <v-btn
        class="font-weight-bold"
        color="white"
        href="https://web.telegram.org//"
        light
        min-width="168"
        target="_blank"
        x-large
      >
        Перейти

        <v-icon right>
          mdi-open-in-new
        </v-icon>
      </v-btn>
    </base-section>
  </v-theme-provider>
</template>

<script>
  export default {
    name: 'SectionNews',

    provide: {
      heading: { align: 'center' },
    },
  }
</script>
