<template>
  <section>
    <component
      :is="`section-${section}`"
      v-for="section in sections"
      :key="section"
    />
  </section>
</template>

<script>
  export default {
    name: 'HomeView',

    props: {
      id: {
        type: String,
        default: 'view',
      },
    },

    data: () => ({
      sections: []
    })
  }
</script>