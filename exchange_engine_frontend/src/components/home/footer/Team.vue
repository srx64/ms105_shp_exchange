<template>
  <v-row dense>
    <v-col
      v-for="(person, index) in team"
      :key="index"
      cols="6"
    >
      <v-card>
        <v-img
          :src="person.photo"
          class="white--text align-end"
          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
          height="200px"
        >
          <template v-slot:placeholder>
            <svg style="width:100%;height:100%" viewBox="0 0 24 24">
              <path fill="grey" d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
            </svg>
          </template>
          <v-card-title
            v-text="person.name"
          />
          <v-card-subtitle
            v-text="person.post"
            class="grey--text text--lighten-2"
          />
        </v-img>

        <v-card-actions>
          <v-btn
            :disabled="!person.description && !person.quote"
            icon
            @click="person.show = !person.show"
          >
            <v-icon>{{ person.show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>

          <v-spacer/>

          <v-btn
            v-for="(social, name) in person.socials"
            :href="social.link"
            target="_blank"
            :color="social.color"
            height="36px"
            fab
            dark
            icon
            small
            :key="name"
          >
            <v-icon
            >
              {{ social.icon }}
            </v-icon>
          </v-btn>
        </v-card-actions>

        <v-expand-transition>
          <v-list-item-content 
            v-show="person.show"
            class="pb-0"
          >
            <v-divider></v-divider>
            <v-card-text v-if="person.description">
              {{ person.description }}
            </v-card-text>
            <v-card-text
              v-if="person.quote"
              class="pt-0"
            >
              <v-card-text
                v-html="person.quote.split('\n').join('<br>')"
                class="font-italic text-center py-0"
              />
              <v-card-subtitle
                class="pt-1 pb-0 text-right font-italic"
              >
                &copy;{{ person.name }}
              </v-card-subtitle>
            </v-card-text>
          </v-list-item-content>
        </v-expand-transition>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'Team',

  data: () => ({
    team: [
      {
        name: 'Мишкина Дарья',
        post: 'Тимлид/Бэкенд-разработчик',
        socials: {},
        photo: '',
        description: '',
        quote: 
          `"Понимаете, Андрей Александрович, мы писали рандом и случайно написали кризис"`,
        show: false
      },
      {
        name: 'Иванченко Антон',
        post: 'Фронтенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/anton_ivanchenko',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
          telegram: 
          {
            link: 'https://t.me/RechnoiD',
            icon: 'mdi-telegram',
            color: '#0088cc'
          }
        },
        photo: '',
        description: '',
        quote:
          `"Андрей Александрович, мы из будущего, не судите строго"`,
        show: false
      },
      {
        name: 'Березин Николай',
        post: 'Фронтенд-разработчик',
        socials: {},
        photo: '',
        description: '',
        quote: 
          `"Я тут ещё ни одного колеса не изобретал, всё хорошо" `,
        show: false
      },
      {
        name: 'Фролов Максим',
        post: 'Бэкенд-разработчик',
        socials: {},
        photo: '',
        description: '',
        quote: 
          `"runservant"`,
        show: false
      }
    ],
    reveal: false,
  }),
}
</script>

<style>
.v-card--reveal {
  bottom: 0;
  opacity: 1 !important;
  position: absolute;
  width: 100%;
}
</style>