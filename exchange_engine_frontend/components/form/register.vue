<template>
  <form>
    <v-text-field
      v-model="userInfo.username"
      :error-messages="usernameErrors"
      label="Логин"
      required
      @input="$v.userInfo.username.$touch()"
      @blur="$v.userInfo.username.$touch()"
      @keyup.enter="$refs.email.focus"
    />
    <v-text-field
      ref="email"
      v-model="userInfo.email"
      :error-messages="emailErrors"
      label="E-mail"
      required
      @input="$v.userInfo.email.$touch()"
      @blur="$v.userInfo.email.$touch()"
      @keyup.enter="$refs.lastName.focus"
    />
    <v-row>
      <v-col>
        <v-text-field
          ref="lastName"
          v-model="userInfo.lastName"
          :error-messages="lastNameErrors"
          label="Фамилия"
          required
          @input="$v.userInfo.lastName.$touch()"
          @blur="$v.userInfo.lastName.$touch()"
          @keyup.enter="$refs.firstName.focus"
        />
      </v-col>
      <v-col>
        <v-text-field
          ref="firstName"
          v-model="userInfo.firstName"
          :error-messages="firstNameErrors"
          label="Имя"
          required
          @input="$v.userInfo.firstName.$touch()"
          @blur="$v.userInfo.firstName.$touch()"
          @keyup.enter="$refs.password.focus"
        />
      </v-col>
    </v-row>
    <v-text-field
      ref="password"
      v-model="userInfo.password"
      :error-messages="passwordErrors"
      label="Пароль"
      required
      :type="showPassword ? 'text' : 'password'"
      :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append="showPassword = !showPassword"
      @input="$v.userInfo.password.$touch()"
      @blur="$v.userInfo.password.$touch()"
      @keyup.enter="$refs.repeatPassword.focus"
    />
    <v-text-field
      ref="repeatPassword"
      v-model="userInfo.repeatPassword"
      :error-messages="repeatPasswordErrors"
      label="Повторите пароль"
      required
      :type="showPassword ? 'text' : 'password'"
      :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append="showPassword = !showPassword"
      @input="$v.userInfo.repeatPassword.$touch()"
      @blur="$v.userInfo.repeatPassword.$touch()"
      @keyup.enter="submit"
    />
    <v-btn
      class="mr-4"
      block
      @click="submit"
    >
      Зарегистрироваться
    </v-btn>
  </form>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'

export default {
  mixins: [validationMixin],

  validations: {
    userInfo: {
      username: { required },
      email: { required, email },
      lastName: { required },
      firstName: { required },
      password: { required },
      repeatPassword: { required }
    }

  },

  props: {
    submitForm: {
      type: Function,
      required: true
    }
  },

  data: () => ({
    userInfo: {
      username: '',
      email: '',
      lastName: '',
      firstName: '',
      password: '',
      repeatPassword: ''
    },
    showPassword: false
  }),

  computed: {
    usernameErrors () {
      const errors = []
      if (!this.$v.userInfo.username.$dirty) { return errors }
      !this.$v.userInfo.username.required && errors.push('Введите логин')
      return errors
    },
    emailErrors () {
      const errors = []
      if (!this.$v.userInfo.email.$dirty) { return errors }
      !this.$v.userInfo.email.email && errors.push('Введите корректный e-mail')
      !this.$v.userInfo.email.required && errors.push('Введите e-mail')
      return errors
    },
    lastNameErrors () {
      const errors = []
      if (!this.$v.userInfo.lastName.$dirty) { return errors }
      !(/^([a-zа-яё]+)$/i.test(this.userInfo.lastName)) && errors.push('Фамилия может содержать только буквы алфавита')
      !this.$v.userInfo.lastName.required && errors.push('Введите фамилию')
      return errors
    },
    firstNameErrors () {
      const errors = []
      if (!this.$v.userInfo.firstName.$dirty) { return errors }
      !(/^([a-zа-яё]+)$/i.test(this.userInfo.firstName)) && errors.push('Имя может содержать только буквы алфавита')
      !this.$v.userInfo.firstName.required && errors.push('Введите имя')
      return errors
    },
    passwordErrors () {
      const errors = []
      if (!this.$v.userInfo.password.$dirty) { return errors }
      !this.$v.userInfo.password.required && errors.push('Введите пароль')
      return errors
    },
    repeatPasswordErrors () {
      const errors = []
      if (!this.$v.userInfo.repeatPassword.$dirty) { return errors }
      !this.$v.userInfo.repeatPassword.required && errors.push('Введите пароль еще раз')
      !(this.userInfo.password === this.userInfo.repeatPassword) && errors.push('Пароли должны совпадать')
      return errors
    }
  },

  methods: {
    submit () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        console.log('ERROR')
      } else {
        this.submitForm(this.userInfo)
      }
    }
  }
}
</script>
