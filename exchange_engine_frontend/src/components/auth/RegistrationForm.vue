<template>
  <div>
    <v-row 
      align="center"
      justify="center"
    >
      <v-card>
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
            />
          
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
              :rules="[v => !!v || 'Подтвердите пароль']"
              :type="'password'"
              name="input-10-1"
              counter
              required
              placeholder="Подтвердите пароль"
              outlined
              dense
            />

            <v-btn
              :disabled="!valid"
              color="success"
              class="mr-7"
              to="/app"
              @click="validate"
            >
              Зарегистрироваться
            </v-btn>
          
            <v-btn
              color="primary"
              outlined
              class="mr-0"
              to="/auth/login"
            >
              Войти
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-row>
  </div>
</template>

<script>
  export default {
    name: 'RegistrationForm',

    data() {
      return {
        valid: true,
        name: '',
        surname: '',
        show: false,
        PasswordRules: [
          v => !!v || 'Введите пароль',
          v => (v && v.length >= 8) || 'Минимум 8 символов',
        ],
        nameRules: [
          v => !!v || 'Введите имя',
          v => (v && v.length <= 15) || 'Максимум 15 символов',
        ],
        email: '',
        emailRules: [
          v => !!v || 'Введите E-mail',
          v => /.+@.+\..+/.test(v) || 'Введите правильный E-mail',
        ],
      }
    },

    methods: {
      validate () {
        this.$refs.form.validate()
      },
      reset () {
        this.$refs.form.reset()
      },
    },
  }
</script>
