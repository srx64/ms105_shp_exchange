<template>
  <h1>
    Buy
  </h1>
</template>

<script>
  export default {
    name: 'Logout',

    methods: {
      logout () {
        this.$store.dispatch('userLogout')
          .then(() => {
            this.$router.push({ name: 'Login' })
          })
      }
    },

    created () {
      this.logout()
    }
  }
</script>