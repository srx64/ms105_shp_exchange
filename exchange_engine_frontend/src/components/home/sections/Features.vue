<template>
  <BaseSection id="features">
    <BaseSectionHeading title="Наши особенности">
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Libero, in! Asperiores, impedit libero. Veniam rerum saepe unde nihil possimus quibusdam esse accusamus mollitia magni fuga.
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
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis illum veniam cum dolores ratione commodi beatae quas maxime, laboriosam excepturi solut!
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
          icon: 'mdi-fountain-pen-tip',
        },
        {
          title: 'Оптимизация',
          icon: 'mdi-cellphone',
        },
        {
          title: 'Оптимизация',
          icon: 'mdi-ice-pop',
        },
        {
          title: 'Поддержка 24/7',
          icon: 'mdi-help-circle-outline',
        },
      ],
    }),
  }
</script>
