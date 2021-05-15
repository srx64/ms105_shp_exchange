<template>
  <v-list>
    <v-list-item
      v-for="person in team"
      :key="person.nick"
    >
      <v-card
        class="mx-auto"
        max-width="344"
      >
        <v-img
          :src="person.photo"
          height="200px"
        ></v-img>

        <v-card-title>
          {{ person.name }}
        </v-card-title>

        <v-card-subtitle>
          {{ person.post }}
        </v-card-subtitle>

        <v-card-text>
          {{ person.description }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

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
    </v-list-item>
  </v-list>
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