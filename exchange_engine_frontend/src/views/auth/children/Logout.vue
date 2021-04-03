<template>
</template>

<script>
  export default {
    methods: {
      logout () {
        this.$store.dispatch('userLogout')
          .then(() => {
            this.$router.push({ name: 'login' })
          })
      }
    },

    created () {
      this.logout()
    }
  }
</script>