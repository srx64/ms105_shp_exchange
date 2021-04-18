<template>
  <RegistrationForm :onReg="onReg"/>
</template>

<script>
  export default {
    name: 'Registration',

    components: {
      RegistrationForm: () => import('@/components/auth/Reg.vue')
    },

    methods: {
      validate () {
        this.$refs.form.validate()
      },
      onReg(data){
        this.$store.dispatch('userReg', {
          email: data.email,
          username: data.username,
          password: data.password,
          password2: data.password2,
        })
        .then(() => {
          this.$router.push({ name: 'Login' })
        })
        .catch(err => {
          console.log(err)
          this.$store.commit({
              type: 'showSnackbar',
              text: 'Введите корректные данные'
            })
        })
      }
    },
  }
</script>
