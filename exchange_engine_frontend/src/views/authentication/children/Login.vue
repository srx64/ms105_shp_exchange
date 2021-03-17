<template>
  <div>
    <LoginForm/>
  </div>
</template>

<script>
  import LoginForm from '@/components/authentication/LoginForm.vue'
  
  export default {
    name: 'Login',

    components: {
      LoginForm
    },
    
    data: () => ({
      name: '',
      show: false,
      email: '',
    }),
  }
</script>
