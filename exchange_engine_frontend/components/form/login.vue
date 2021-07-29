<template>
  <form>
    <v-text-field
      v-model="userInfo.login"
      :error-messages="loginErrors"
      label="Логин"
      required
    />
    <v-text-field
      v-model="userInfo.password"
      :error-messages="passwordErrors"
      label="Пароль"
      required
      :type="showPassword ? 'text' : 'password'"
      :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append="showPassword = !showPassword"
    />

    <v-btn
      class="mr-4"
      block
      @click="submit"
    >
      Войти
    </v-btn>
  </form>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {
  mixins: [validationMixin],
  props: {
    submitForm: {
      type: Function,
      required: true
    }
  },
  validations: {
    userInfo: {
      login: { required },
      password: { required }
    }
  },
  data: () => ({
    userInfo: {
      login: '',
      password: ''
    },
    showPassword: false
  }),

  computed: {
    loginErrors () {
      const errors = []
      if (!this.$v.userInfo.login.$dirty) { return errors }
      !this.$v.userInfo.login.required && errors.push('Login is required.')
      return errors
    },
    passwordErrors () {
      const errors = []
      if (!this.$v.userInfo.password.$dirty) { return errors }
      !this.$v.userInfo.password.required && errors.push('Password is required')
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
