<template>
  <div>
    <v-autocomplete
      v-model="model"
      :items="items"
      :loading="isLoading"
      :search-input.sync="search"
      color="grey darken-4"
      hide-no-data
      hide-selected
      item-text="Description"
      item-value="API"
      label="Поиск"
      placeholder="Начните вводить текст для поиска"
      prepend-icon="mdi-magnify"
      return-object
    />
    <v-row>
      <v-col cols="auto">
        <v-btn elevation="0" to="/exchange/сatalog/stocks">
          Акции
        </v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn disabled elevation="0">
          Облигации
        </v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn disabled elevation="0">
          Валюты
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data: () => ({
    descriptionLimit: 60,
    entries: [],
    isLoading: false,
    model: null,
    search: null
  }),

  computed: {
    fields () {
      if (!this.model) {
        return []
      }

      return Object.keys(this.model).map((key) => {
        return {
          key,
          value: this.model[key] || 'n/a'
        }
      })
    },
    items () {
      return this.entries.map((entry) => {
        const Description = entry.Description.length > this.descriptionLimit
          ? entry.Description.slice(0, this.descriptionLimit) + '...'
          : entry.Description

        return Object.assign({}, entry, {
          Description
        })
      })
    }
  },

  watch: {
    model (val) {
      if (val != null) {
        this.$router.push({
          name: 'exchange-stocks-id',
          params: {
            id: 1
          }
        })
      }
    },
    search (val) {
      // Items have already been loaded
      if (this.items.length > 0) {
        return
      }

      // Items have already been requested
      if (this.isLoading) {
        return
      }

      this.isLoading = true

      // Lazily load input items
      fetch('https://api.publicapis.org/entries')
        .then(res => res.json())
        .then((res) => {
          const {
            count,
            entries
          } = res
          this.count = count
          this.entries = entries
        })
        .catch((err) => {
          console.log(err)
        })
        .finally(() => (this.isLoading = false))
    }
  }
}

</script>
