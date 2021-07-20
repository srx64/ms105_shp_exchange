<template>
  <v-app-bar
    id="home-app-bar"
		app
		elevation="1"
		elevate-on-scroll
		height="80"
	>
		<BaseImg
			:src="require('@/assets/logo_shp_exchange_horizontal.png')"
      contain
      max-width="150"
      width="100%"
		/>

		<v-spacer/>

		<div >
			<BaseBtn
				to="auth/login"
				class="ma-2"
				weight="regular"
				text
			>
				Войти
			</BaseBtn>

			<BaseBtn
				to="auth/reg"
				class="ma-2 hidden-sm-and-down"
				weight="regular"
			>
				Создать аккаунт
			</BaseBtn>
		</div>
  </v-app-bar>
</template>

<script>
	export default {
		name: 'HomeAppBar'
	}
</script>