<template>
  <v-card
    class="mx-auto my-12"
    max-width="500"
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

    <v-card-text
      class="pb-0"
    >

    <validation-observer
    ref="observer"
    v-slot="{ invalid }">

      <v-form>
        <validation-provider
          v-slot="{ errors }"
          name="Никнейм"
          rules="required|max:15|min:3"
        >
          <v-text-field
            v-model="username"
            :counter="15"
            :error-messages="errors"
            label="Никнейм"
            placeholder="Введите никнейм"
            required
            outlined
            dense

          ></v-text-field>
        </validation-provider>
        <validation-provider
          v-slot="{ errors }"
          name="E-mail"
          rules="required|email"
        >
          <v-text-field
            v-model="email"
            :error-messages="errors"
            label="E-mail"
            placeholder="Введите E-mail"
            required
            outlined
            dense

          ></v-text-field>
        </validation-provider>

        <validation-provider
          v-slot="{ errors }"
          name="password"
          rules="required|password:@confirm"
        >
          <v-text-field
            v-model="password"
            :error-messages="errors"
            label="Пароль"
            placeholder="Введите пароль"
            :type="show ? 'text' : 'password'"
            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="show = !show"
            required
            outlined
            dense

          ></v-text-field>
        </validation-provider>

        <validation-provider
          v-slot="{ errors }"
          name="confirm"
          rules="required"
        >
          <v-text-field
            v-model="password2"
            :type="false ? 'text' : 'password'"
            :error-messages="errors"
            label="Подтверждение"
            name="Подтверждение"
            placeholder="Подтвердите пароль"
            required
            outlined
            dense
          ></v-text-field>
        </validation-provider>
        
        <v-divider class="mx-4"></v-divider>

      <v-container 
        class="d-flex flex-wrap justify-space-between pa-0">

        <v-btn
              @click="register"
              color="primary"
              class="mx-auto my-3"
              :disabled="invalid"
            >
              Создать аккаунт
            </v-btn>

            <v-btn
              to="/auth/login"
              color="primary"
              class="mx-auto my-3"
              outlined
            >
              Войти
            </v-btn>
        </v-container>
    </v-form>
  </validation-observer>

    </v-card-text>
  </v-card>
</template>

<script>
import { required, email, max, min } from 'vee-validate/dist/rules'
import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'

setInteractionMode('eager')

  extend('required', {
    ...required,
    message: 'Это поле не может быть пустым',
  })

  extend('max', {
    ...max,
    message: 'Поле "{_field_}" не может быть больше {length} символов',
  })

  extend('min', {
    ...min,
    message: 'Поле "{_field_}" не может быть меньше {length} символов',
  })

  extend('email', {
    ...email,
    message: 'Введите корректный E-mail',
  })

  extend('password', {
  params: ['target'],
  validate(value, { target }) {
    return value === target;
  },
  message: 'Пароли не совпадают'
});

  export default {
    name: 'RegForm',
    props: [
      'onReg',
    ],

    components: {
      ValidationProvider,
      ValidationObserver,
    },

    data() {
      return {
        username: '',
        email: '',
        password: '',
        password2: '',
        show: false,
      }
    },
    methods: {
      // submit () {
      //   this.$refs.observer.validate()
      // },
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
