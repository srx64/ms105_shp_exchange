<template>
  <v-app>
		<AppBar/>
		
		<AppView/>
  </v-app>
</template>

<script>
  export default {
		name: 'AppLayout',

		components: {
			AppBar: () => import('@/layouts/app/AppBar'),
			AppView: () => import('@/layouts/app/View')
		}
  }
</script>