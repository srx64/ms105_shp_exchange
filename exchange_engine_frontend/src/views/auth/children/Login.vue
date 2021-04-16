<template>
  <div>
    <LoginForm :onLogin="onLogin"/>

    <template>
      <v-snackbar
        v-model="snackbar"
        timeout="1000"
        color="blue darken-2"
      >
        {{ text }}

        <template v-slot:action="{ attrs }">
          <v-btn
            color="red"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
            Закрыть
          </v-btn>
        </template>
      </v-snackbar>
    </template>
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
      snackbar: false,
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
          this.snackbar = true
          data.incorrectAuth = true
        })
      }
    }
  }
</script>
