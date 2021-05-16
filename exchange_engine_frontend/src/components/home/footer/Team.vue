<template>
  <v-row dense>
    <v-col
      v-for="person in team"
      :key="person.nick"
      cols="6"
    >
      <v-card>
        <v-img
          :src="person.photo"
          class="white--text align-end"
          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
          height="200px"
        >
          <v-card-title v-text="person.name"></v-card-title>
        </v-img>

        <v-card-actions>

          

          <v-btn
            icon
            @click="person.show = !person.show"
          >
            <v-icon>{{ person.show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
        </v-card-actions>

        <v-expand-transition>
          <div v-show="person.show">
            <v-divider></v-divider>

            <v-card-text
              class="font-italic"
            >
              "{{ person.quote }}"
            </v-card-text>
          </div>
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
        nick: 'Rechnoi',
        name: 'Иванченко Антон',
        post: 'Фронтенд-разработчик',
        photo: 'https://i.pinimg.com/564x/0f/14/85/0f148590b392d21b4cc7d1d51193dc45.jpg',
        description: 'Описание',
        quote: 'Хехе, работает',
        socials: [

        ],
        show: false
      },
      {
        nick: 'vortexof',
        name: 'Мишкина Дарья',
        post: 'Тимлид Бэкенд-разработчик',
        photo: 'https://i.pinimg.com/564x/0f/14/85/0f148590b392d21b4cc7d1d51193dc45.jpg',
        description: 'Описание',
        quote: 'Хехе, работает',
        show: false
      },
      {
        nick: 'Berezin',
        name: 'Березин Николай',
        post: 'Фронтенд-разработчик',
        photo: 'https://i.pinimg.com/564x/0f/14/85/0f148590b392d21b4cc7d1d51193dc45.jpg',
        description: 'Описание',
        quote: 'Фисштех ❤',
        show: false
      },
      {
        nick: 'Frolov',
        name: 'Фролов Максим',
        post: 'Бэкенд-разработчик',
        photo: 'https://i.pinimg.com/564x/0f/14/85/0f148590b392d21b4cc7d1d51193dc45.jpg',
        description: 'Описание',
        quote: 'Хехе, работает',
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