<template>
  <div>
      <Hero/>
      <v-sheet
        id="features"
        class="secondary"
      >
        <v-responsive
          class="mx-auto"
          max-width="1350"
          tile
        >
          <v-container fluid>
            <v-row>
              <v-col
                v-for="card in cards"
                :key="card.title"
                cols="12"
                sm="4"
                md="3"
              >
                <base-info-card
                  align="center"
                  dark
                  v-bind="card"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-responsive>
      </v-sheet>
  </div>
</template>

<script>
  import Hero from '@/components/home/Hero.vue'

  export default {
    name: 'Home',

    metaInfo: { title: 'Home' },

    components: {
      Hero
    },

    data() {
      return {
        cards: [
          {
            icon: 'mdi-keyboard-outline',
            title: 'Trendy Design',
            text: 'Curabitur aliquet quam id dui posuere blandit. Nulla quis lorem ut libero malesuada feugiat.'
          },
          {
            icon: 'mdi-camera-outline',
            title: 'Photography',
            text: 'Curabitur aliquet quam id dui posuere blandit. Nulla quis lorem ut libero malesuada feugiat.'
          },
          {
            icon: 'mdi-pencil-outline',
            title: 'Brand Making',
            text: 'Curabitur aliquet quam id dui posuere blandit. Nulla quis lorem ut libero malesuada feugiat.'
          },
          {
            icon: 'mdi-puzzle-outline',
            title: 'Поддержка 24/7',
            text: 'Curabitur aliquet quam id dui posuere blandit. Nulla quis lorem ut libero malesuada feugiat.'
          },
        ],
      }
    }
  }
</script>
