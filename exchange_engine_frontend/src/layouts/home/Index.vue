<template>
  <v-app>
		<HomeAppBar/>
		
		<HomeView/>

		<HomeFooter/>
  </v-app>
</template>

<script>
  export default {
		name: 'HomeLayout',

		components: {
			HomeAppBar: () => import('@/layouts/home/AppBar'),
			HomeFooter: () => import('@/layouts/home/Footer'),
			HomeView: () => import('@/layouts/home/View')
		}
  }
</script>