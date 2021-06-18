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
          height="300px"
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
        socials: {
          telegram: {
            link: 'https://t.me/vortexof',
            icon: 'mdi-telegram',
            color: '#0088cc'
          }
        },
        photo: require('@/assets/team/mishkina.jpg'),
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
          telegram: {
            link: 'https://t.me/RechnoiD',
            icon: 'mdi-telegram',
            color: '#0088cc'
          }
        },
        photo: require('@/assets/team/ivanchenko.jpg'),
        description: '',
        quote:
          `"Андрей Александрович, мы из будущего, не судите строго"`,
        show: false
      },
      {
        name: 'Березин Николай',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/id307666016',
            icon: 'mdi-vk',
            color: '#2787F5'
          }
        },
        photo: require('@/assets/team/berezin.jpg'),
        description: '',
        quote: 
          `"Я тут ещё ни одного колеса не изобретал, всё хорошо" `,
        show: false
      },
      {
        name: 'Снадкин Даниил',
        post: 'Бэкенд-разработчик/Фронтенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/sndkdanya',
            icon: 'mdi-vk',
            color: '#2787F5'
          }
        },
        photo: require('@/assets/team/snadkin.jpg'),
        description: '',
        quote: 
          `"Тайна тридцать второго теста"`,
        show: false
      },
      {
        name: 'Фролов Максим',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/mi_x_im',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
          telegram: {
            link: 'https://t.me/mi_x_im',
            icon: 'mdi-telegram',
            color: '#0088cc'
          }
        },
        photo: require('@/assets/team/frolov.jpg'),
        description: '',
        quote: 
          `"runservant"`,
        show: false
      },
      {
        name: 'Баранов Юрий',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/uranbee',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: '',
        description: '',
        quote: 
          `"У меня вырос монокль"`,
        show: false
      },
      {
        name: 'Голубев Артем',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/ddodgers',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: require('@/assets/team/golubev.jpg'),
        description: '',
        quote: 
          `"Здесь могла быть ваша реклама"`,
        show: false
      },
      {
        name: 'Кузьмичев Артем',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/id431884327',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: '',
        description: '',
        quote: 
          ``,
        show: false
      },
      {
        name: 'Бурнашева Мария',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/maaaassh',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: require('@/assets/team/burnasheva.png'),
        description: '',
        quote: 
          `"Проект без жертв"`,
        show: false
      },
      {
        name: 'Кочерова Влада',
        post: 'Бэкенд-разработчик/Госпожа помянем',
        socials: {
          vk: {
            link: 'https://vk.com/maybeyoursmaybenot',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: require('@/assets/team/kocherova.jpeg'),
        description: '',
        quote: 
          `"Утиная магия"`,
        show: false
      },
      {
        name: 'Бетуганов Арсен',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/alonew1thyourself',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: require('@/assets/team/betuganov.jpg'),
        description: '',
        quote: 
          ``,
        show: false
      },
      {
        name: 'Выходцев Александр',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/id448788329',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: '',
        description: '',
        quote: 
          ``,
        show: false
      },
      {
        name: 'Комаров Кирилл',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/kirillkoms',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: require('@/assets/team/komarov.jpg'),
        description: '',
        quote: 
          `"Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили"`,
        show: false
      },
      {
        name: 'Ганин Влад',
        post: 'Бэкенд-разработчик',
        socials: {
          vk: {
            link: 'https://vk.com/traumt_liebe',
            icon: 'mdi-vk',
            color: '#2787F5'
          },
        },
        photo: require('@/assets/team/ganin.jpg'),
        description: '',
        quote: 
          `"На самом деле не знаю, но можно error 404"`,
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