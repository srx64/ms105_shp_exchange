<template>
  <div>
    <LoginForm :onLogin="onLogin"/>
  </div>
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
      text: 'Ошибка! Неверный логин или пароль!'
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
          this.$store.commit({
            type: 'showSnackbar',
            text: 'Неправильный логин или пароль'
          })
          data.incorrectAuth = true
        })
      }
    }
  }
</script>
