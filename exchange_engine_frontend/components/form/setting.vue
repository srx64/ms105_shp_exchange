<template>
  <v-form v-model="valid">
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="userInfo.firstName" :error-messages="firstNameErrors" label="Имя" required />
      </v-col>

      <v-col cols="12" md="6">
        <v-text-field v-model="userInfo.lastname" :error-messages="lastNameErrors" label="Фамилия" required />
      </v-col>
      <v-col cols="12">
        <v-text-field v-model="userInfo.login" :error-messages="loginErrors" label="Логи" required />
      </v-col>
      <v-col cols="12">
        <v-text-field v-model="userInfo.email" :error-messages="emailErrors" label="E-mail" required />
      </v-col>
    </v-row>
    <v-btn class="mr-4" block color="primary" @click="submit">
      Сохранить
    </v-btn>
  </v-form>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'

export default {
  mixins: [validationMixin],

  validations: {
    userInfo: {
      login: { required },
      email: { required, email },
      lastName: { required },
      firstName: { required }
    }

  },

  props: {
    submitForm: {
      type: Function,
      required: true
    }
  },

  data: () => ({
    showPassword: false
  }),

  computed: {
    userInfo () {
      return {
        login: '',
        email: '',
        lastName: '',
        firstName: '',
        password: ''
      }
    },
    loginErrors () {
      const errors = []
      if (!this.$v.userInfo.login.$dirty) { return errors }
      !this.$v.userInfo.login.required && errors.push('Введите логин')
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

<style>

</style>
