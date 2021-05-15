<template>
  <v-dialog
    :width="width"
    v-model="dialog"
  >
    <template v-slot:activator="{ on, attrs }">
      <a
        class="white--text pa-1 pa-md-0"
        v-text="title"
        v-bind="attrs"
        v-on="on"
      /> 
    </template>

    <v-card>
      <v-card-title 
        class="headline grey lighten-2"
      >
        {{ title }}
      </v-card-title>

      <v-card-text
        class="mt-2"
      >
        <slot/>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          text
          @click="dialog = false"
        >
          Закрыть
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    name: 'BaseDialog',

    props: {
      dialog: {
        type: Boolean,
        default: false,
      },
      title: String,
      width: {
        type: [String, Number],
        default: 700
      }
    },
  }
</script>
