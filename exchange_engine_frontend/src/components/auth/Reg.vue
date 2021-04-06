<template>
  <v-card
    class="mx-auto"
  >
    <v-toolbar
      flat
      color="blue darken-2"
      dark
    >
      <v-toolbar-title>
        Регистрация
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-form
        ref="form"
        v-model="valid"
        lazy-validation
      >
        <v-text-field
          v-model="username"
          :rules="nameRules"
          label="Никнейм"
          required
          placeholder="Введите имя"
          outlined
          dense
        />
<!-- 
        <v-text-field
          v-model="name"
          :rules="nameRules"
          label="Имя"
          required
          placeholder="Введите имя"
          outlined
          dense
        />

        <v-text-field
          v-model="surname"
          :rules="nameRules"
          label="Фамилия"
          required
          placeholder="Введите фамилию"
          outlined
          dense
        /> -->
      
        <v-text-field
          v-model="email"
          :rules="emailRules"
          label="E-mail"
          required
          placeholder="Введите E-mail"
          outlined
          dense
        />

        <v-text-field
          v-model="password"
          label="Пароль"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="PasswordRules"
          :type="show ? 'text' : 'password'"
          name="input-10-1"
          hint="Минимум 8 символов"
          counter
          required
          @click:append="show = !show"
          placeholder="Введите пароль"
          outlined
          dense
        />

        <v-text-field
          label="Подтвердите пароль"
          v-model="password2"
          :rules="[v => !!v || 'Подтвердите пароль']"
          :type="'password'"
          name="input-10-1"
          counter
          required
          placeholder="Подтвердите пароль"
          outlined
          dense
        />

        <v-row>
          <v-col
            cols="12"
            md="6"
          >
            <v-btn
              v-on:click="register"
              color="success"
            >
              Зарегистрироваться
            </v-btn>
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-btn
              color="primary"
              outlined
              to="/auth/login"
            >
              Войти
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    name: 'RegForm',
    props: [
      'onReg',
    ],

    data() {
      return {
        username: '',
        email: '',
        password: '',
        password2: '',
        show: false,
        PasswordRules: [
          v => !!v || 'Введите пароль',
          v => (v && v.length >= 8) || 'Минимум 8 символов',
        ],
        nameRules: [
          v => !!v || 'Введите имя',
          v => (v && v.length <= 15) || 'Максимум 15 символов',
        ],
        emailRules: [
          v => !!v || 'Введите E-mail',
          v => /.+@.+\..+/.test(v) || 'Введите правильный E-mail',
        ],
      }
    },
    methods: {
      register() { 
        this.onReg({
          email: this.email,
          username: this.username,
          password: this.password,
          password2: this.password2,
        })
      }
    }
  }
</script>
