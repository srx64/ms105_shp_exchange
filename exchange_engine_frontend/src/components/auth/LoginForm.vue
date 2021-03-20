<template>
  <div>
    <v-row 
      align="center"
      justify="center"
    >
      <v-card style="margin: 0px; padding: 0px; width: 450px;">
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
            
            <v-btn
              color="success"
              to="/app"
              class="mr-15"
              @click="validate"
            >
              Войти
            </v-btn>

            <v-btn
              color="primary"
              outlined
              class="mr-0"
              to="/auth/registration"
            >
              Зарегестрироваться
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-row>
  </div>
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
