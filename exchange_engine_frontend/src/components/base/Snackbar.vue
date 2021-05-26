<template>
  <v-snackbar
    v-model="enable"
    :timeout="timeout"
    :class="classes"
    :color="color"
    :dark="dark"
    v-bind="$attrs"
    v-on="$listeners"
  >
    {{ text }}

    <template v-slot:action="{ attrs }">
        <v-btn
          @click="enable = false"
          icon
          v-bind="attrs"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
  </v-snackbar>
</template>

<script>
  export default {
    name: 'BaseSnackbar',

    props: {
      color: {
        type: String,
        default: 'blue darken-2'
      },
      dark: {
        type: Boolean,
        default: false
      },
      timeout: {
        type: [Number, String],
        default: 3000
      },
      align: {
        type: String,
        default: 'left'
      }
    },

    data: () => ({
      enable: false,
      text: '',
    }),

    created () {
      this.$store.subscribe((mutation, state) => {
        if (mutation.type === 'showSnackbar') {
          this.enable = true
          this.text = state.snackbar.snackbarText
        }
      })
    },

    computed: {
      classes () {
        const classes = [
          `text-${this.align}`
        ]

        return classes
      }
    }
  }
</script>