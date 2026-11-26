<template>
	<div class="">
	<p><router-link to="/signup/" class="hover hover--link">Sign up</router-link> to receive our latest insights, news and work.</p>
		<!-- <form ref="form" action="" class="signup">
			<div class="u-flex">
				<input v-model="form.name" class="input" type="text" @focus="onFocus" @blur="onBlur">
			<img class="arrow" src="../../assets/arrow-right.svg">
			</div>
		</form> -->
	</div>
</template>

<script>
	export default {
		data() {
			return {
				form: {
					name: ''
				}
			}
		},
		mounted() {

		},
		destroyed() {

		},
		methods: {

		}
	}
</script>

<style scoped lang="scss">
	p {
		margin: 0;
	}
</style>


// WEBPACK FOOTER //
// src/components/modules/SignupTrigger.vue