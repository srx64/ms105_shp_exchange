<template>
    <div>
        <v-card
            class="mx-auto"
            max-width="380"
        >
            <v-list-item three-line>
                <v-list-item-content>
                    <div class="overline mb-4">
                        Your name
                    </div>

                    <v-list-item-title class="headline mb-1">
                        Developer
                    </v-list-item-title>

                    <v-list-item-subtitle>Lorem ipsum dolor sit amet, consectetur adipiscing elit Integer sit amet mi blandit, molestie tortor ac, lacinia sem. Cras id scelerisque neque. Lorem ipsum dolor sit amet, consectetur adipiscing elit Integer sit amet mi blandit, molestie tortor ac, lacinia sem. Cras id scelerisque neque.Curabitur eget tortor eu purus tristique ultrices in sit amet tortor. Proin nisi metus, sodales ac velit a, tempor rhoncus nisi. Aliquam eget urna libero. Proin ac tellus non nisi consectetur efficitur ultricies vestibulum metus. Cras eget imperdiet lacus.</v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-avatar
                    tile
                    size="80"
                    color="grey"
            ></v-list-item-avatar>
            </v-list-item>
            
            <v-card-actions>
            <v-btn
                text
                color="teal accent-4"
                @click="reveal = true"
            >
                Learn More
            </v-btn>
            </v-card-actions>

            <v-expand-transition>
            <v-card
                v-if="reveal"
                class="transition-fast-in-fast-out v-card--reveal"
                style="height: 100%"
            >
                <v-card-text class="pb-0">
                <div class="overline mb-4">
                    Your name
                </div>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer sit amet mi blandit, molestie tortor ac, lacinia sem. Cras id scelerisque neque. </p>
                </v-card-text>
                
                <v-card-actions class="pt-0">
                <v-btn
                    text
                    color="teal accent-4"
                    @click="reveal = false"
                >
                    Close
                </v-btn>
                </v-card-actions>
            </v-card>
            </v-expand-transition>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'Team',
        data: () => ({
            reveal: false,
    }),
    }
</script>

<style>
.v-card--reveal {
  bottom: 0;
  opacity: 1 !important;
  position: absolute;
  width: 100%;
}
</style>