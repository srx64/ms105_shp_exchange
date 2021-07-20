<script>
  import View from '@/views/home/View'
  import LoadSections from '@/mixins/load-sections'

  export default {
    name: 'Home',

    metaInfo: {
      title: 'Главная',
    },

    extends: View,

    mixins: [
      LoadSections([
        'hero',
        'features',
        'social-media'
      ]),
    ]
  }
</script>