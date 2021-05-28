<template>
  <v-card
    class="mx-auto my-12"
    max-width="400"
  >
    <v-toolbar
      flat
      color="blue darken-2"
      dark
    >
      <v-toolbar-title>
        Вход
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text
      class="pb-0"
    >
      <v-form
        ref="form"
        lazy-validation
        
            
      >
        <v-text-field 
          v-model="username"
          @keyup.enter="$refs.password.focus"
          ref="login"
          label="Имя пользователя"
          placeholder="Введите имя пользователя"
          required
          outlined
          dense
        />

        <v-text-field
          v-model="password"
          @keyup.enter="login"
          ref="password"
          label="Пароль"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show ? 'text' : 'password'"
          name="input-10-1"
          @click:append="show = !show"
          placeholder="Введите пароль"
          outlined
          required
          dense
        />

        <v-divider class="mx-4"></v-divider>

        <v-container 
          class="d-flex flex-wrap justify-space-between pa-0"
        >
          <v-btn
            @click="login"
            color="primary"
            class="mx-auto my-3"
          >
            Войти
          </v-btn>

          <v-btn
            to="/auth/reg"
            color="primary"
            class="mx-auto my-3"
            outlined
          >
            Создать аккаунт
          </v-btn>
        </v-container>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    name: 'LoginForm',

    props: [
      'onLogin'
    ],

    data: () => ({
      username: '',
      password: '',
      show: false,
      incorrectAuth: false
    }),

    methods: {
      login() { 
        this.onLogin({
          username: this.username,
          password: this.password,
          incorrectAuth: this.incorrectAuth
        })
      },
      submit () {
        console.log('hey')
      }
    }
  }
</script>
