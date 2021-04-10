<template>
  <LoginForm :onLogin="onLogin"/>
</template>

<script>
  export default {
    name: 'Login',

    components: {
      LoginForm: () => import('@/components/auth/Login.vue')
    },
    
    data: () => ({
      name: '',
      show: false,
      email: '',
    }),

    methods: {
      onLogin(data) {
        this.$store.dispatch('userLogin', {
          username: data.username,
          password: data.password
        })
        .then(() => {
          this.$router.push({ name: 'App' })
        })
        .catch(err => {
          console.log(err)
          alert('Ошибка! Возможно введен неверный логин или пароль')
          data.incorrectAuth = true
        })
      }
    }
  }
</script>
