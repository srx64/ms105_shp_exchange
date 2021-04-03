<template>
  <RegistrationForm/>
</template>

<script>
  export default {
    name: 'Registration',

    components: {
      RegistrationForm: () => import('@/components/auth/Reg.vue')
    },

    data() {
      return {
        valid: true,
        name: '',
        show: false,
        PasswordRules: [
          v => !!v || 'Введите пароль',
          v => (v && v.length <= 8) || 'Минимум 8 символов',
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
