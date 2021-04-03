<template>
  <v-app-bar
    id="home-app-bar"
		app
		elevation="1"
		elevate-on-scroll
		height="80"
	>
		<BaseImg
			:src="require('@/assets/logo.png')"
      contain
      max-width="46"
      width="100%"
		/>

		<v-spacer/>

		<div 
		
		>
			<BaseBtn
				to="auth/login"
				class="d-inline-flex pa-2"
        height="auto"
				text
			>
				Войти
			</BaseBtn>

			<BaseBtn
				to="auth/registration"
				class="ma-2"
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