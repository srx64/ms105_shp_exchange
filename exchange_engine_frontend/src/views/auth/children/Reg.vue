<template>
  <RegistrationForm :onReg="onReg"/>
</template>

<script>
// import axios from 'axios'
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
      }
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
      }
    },
  }
</script>
