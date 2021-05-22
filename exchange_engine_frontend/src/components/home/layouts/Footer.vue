<template>
  <v-footer
    id="home-footer"
    color="black"
    dark
    min-height="72"
  >
    <v-container>
      <v-row>
        <v-col
          cols="12"
          md="6"
        >
          <div
            class="d-flex flex-wrap justify-md-start justify-center justify-md-none"
          >
            <div
              v-for="(dialog, i) in dialogs"
              :key="dialog.title"
              class="text-center"
            >
              <BaseDialog
                :dialog="dialog.state"
                :title="dialog.title"
                width="1000"
              >
                <component
                  :is="dialog.component"
                />
              </BaseDialog>
              <span
                v-if="i < dialogs.length - 1"
                class="d-inline-block mx-3"
              >
                |
              </span>
            </div>
          </div>
        </v-col>
        <v-col
          cols="12"
          md="6"
          class="text-center text-md-right"
        >
          &copy; 2021 Exchange engine
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
  export default {
    name: 'Home',

    components: {
      About: () => import('@/components/home/footer/About.vue'),
      Team: () => import('@/components/home/footer/Team.vue'),
      Rules: () => import('@/components/home/footer/Rules.vue')
    }, 

    data: () => ({
      dialogs: [
        {
          title: 'О нас',
          state: false,
          component: 'About'
        },
        {
          title: 'Наша команда',
          state: false,
          component: 'Team'
        },
        {
          title: 'Правила',
          state: false,
          component: 'Rules'
        },
      ],
    }),
  }
</script>