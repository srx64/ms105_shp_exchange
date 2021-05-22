<template>
  <BaseSection id="features">
    <BaseSectionHeading title="Наши особенности">
      Проект создан для начинающих инвесторов в целях обучения и практики. В нашем сервисе вы может попробовать базовые 
      инструменты торговли на бирже и собрать свой собственный виртуальный портфель. Все сделки производятся с виртуальной 
      валютой, в случае ошибки вы ничем не рискуете.
    </BaseSectionHeading>

    <v-container
      class="py-15"
    >
      <v-row>
        <v-col
          v-for="(feature, i) in features"
          :key="i"
          cols="12"
          md="6"
        >
          <BaseAvatarCard
            v-bind="feature"
            align="left"
            horizontal
          >
            {{ feature.description }}
          </BaseAvatarCard>
        </v-col>
      </v-row>
    </v-container>
  </BaseSection>
</template>

<script>
  export default {
    name: 'SectionThemeFeatures',

    data: () => ({
      features: [
        {
          title: 'Удобный интерфейс',
          icon: 'mdi-monitor-screenshot',
          description: 'Интуитивно понятный интерфейс для удобства работы',
        },
        {
          title: 'Оптимизация',
          icon: 'mdi-cellphone-link',
          description: 'Сайт оптимизирован под мобильные устройства',
        },
        {
          title: 'Доступность',
          icon: 'mdi-feather',
          description: 'СОздать аккаунт может кто угодно, без ограничений',
        },
        {
          title: 'Поддержка 24/7',
          icon: 'mdi-hours-24',
          description: 'Наша отзывчивая поддержка ответит на любой вопрос',
        },
      ],
    }),
  }
</script>
