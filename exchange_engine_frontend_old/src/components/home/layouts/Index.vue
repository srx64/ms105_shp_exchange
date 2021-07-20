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
			HomeAppBar: () => import('@/components/home/layouts/AppBar'),
			HomeFooter: () => import('@/components/home/layouts/Footer'),
			HomeView: () => import('@/components/home/layouts/View')
		}
  }
</script>