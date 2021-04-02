<template>
  <component>
    :is="tag"
  </component>
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