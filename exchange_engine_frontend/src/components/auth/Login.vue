<template>
  <v-card>
    <v-toolbar
      flat
      color="blue darken-2"
      dark
    >
      <v-toolbar-title>
        Вход
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-form
        ref="form"
        lazy-validation
      >
        <v-text-field
          v-model="email"
          label="Почта"
          placeholder="Введите E-mail"
          required
          outlined
          dense
        />

        <v-text-field
          v-model="password"
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
        
        <v-row>
          <v-col
            cols="12"
            md="6"
          >
            <v-btn
              color="success"
              to="/app"
              @click="validate"
            >
              Войти
            </v-btn>
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-btn
              color="primary"
              outlined
              to="/auth/reg"
            >
              Зарегистрироваться
            </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    name: 'LoginForm',
    data: () => ({
      email: '',
      show: false,
      password: '',
    }),
  }
</script>
