<template>
 <h1> in develop </h1>
</template>

<script>
  export default {
    name: 'BaseHeading',

    props: {
      align: {
        type: String,
        default: 'left'
      },
      size: {
        type: String,
        default: 'text-h3'
      },
      space: {
        type: [Number, String],
        default: 4
      },
      
    }
  }
</script>