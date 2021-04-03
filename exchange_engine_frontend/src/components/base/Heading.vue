<template>
  <component
    :is="tag"
    :class="classes"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <slot/>
  </component>
</template>

<script>
  export default {
    name: 'BaseHeading',

    inject: {
      theme: {
        default: () => ({ isDark: false }),
      },
    },

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
      mobileSize: {
        type: String,
        default: 'text-h4'
      },
      mobileBreakpoint: {
        type: [Number, String],
        default: 768
      },
      tag: {
        type: String,
        default: 'h1'
      },
      weight: {
        type: String,
        default: 'black'
      },
    },

    computed: {
      fontSize () {
        return this.$vuetify.breakpoint.width >= this.mobileBreakpoint
          ? this.size
          : this.mobileSize
      },
      classes () {
        const classes = [
          this.fontSize,
          `font-weight-${this.weight}`,
          `mb-${this.space}`,
          `text-${this.align}`,
          this.theme.isDark && 'white--text',
        ]

        return classes
      }
    }
  }
</script>
