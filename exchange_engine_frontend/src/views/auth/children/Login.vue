<template>
  <LoginForm/>
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
  }
</script>
