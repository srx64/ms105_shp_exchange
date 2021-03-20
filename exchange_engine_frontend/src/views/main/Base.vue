<template>
  <div>
    <Header/>
    <v-main>
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
    </v-main>
    <Footer/>
  </div>
</template>

<script>
  import Header from '@/components/main/Header.vue'
  import Hero from '@/components/main/Hero.vue'
  import Footer from '@/components/main/Footer.vue'

  export default {
    name: 'Main',

    components: {
      Header, Hero, Footer
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
