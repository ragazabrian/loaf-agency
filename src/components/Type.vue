<template>
  	<div class="Type">
						
		</iframe>

	  	<div class="entry">
	  	<h1>Loaf is an agile, mediocrity slaying creative studio, powered by the beautiful idea.</h1>
		</div>

		<div class="entry">
	  	<h2>Loaf is an agile, mediocrity slaying creative studio, powered by the beautiful idea.</h2>
		</div>

		<div class="entry">
	  	<h3>Loaf is an agile, mediocrity slaying creative studio, powered by the beautiful idea.</h3>
		</div>

		<div class="entry">
	  	<h4>Loaf is an agile, mediocrity slaying creative studio, powered by the beautiful idea.</h4>
		</div>

		<div class="entry">
	  	<p>Loaf is an agile, mediocrity slaying creative studio, powered by the beautiful idea.</p>
		
	  		<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur magna arcu, rutrum et lobortis nec, fringilla sed nisl. Praesent nibh velit, cursus non feugiat nec, suscipit semper velit. Pellentesque libero purus, euismod in erat et, ornare accumsan quam. Pellentesque nec blandit neque. Nam mi nulla, posuere a iaculis ut, consectetur sed libero. Aliquam commodo lorem urna, id lacinia nibh tempor in. Nulla eget semper nunc. Nulla a sem rhoncus, cursus elit vitae, condimentum ex. Quisque pretium ligula justo, id congue elit porttitor nec. Quisque ultricies lectus diam, at consequat diam mattis vel. Quisque euismod ultricies lectus vel vehicula. Ut sed lectus quis orci faucibus efficitur ac vitae dui. Praesent eu enim ut elit venenatis vulputate eget bibendum sapien. Nulla blandit, magna quis elementum iaculis, ex turpis egestas quam, et commodo leo nisl in lacus.</p>

			<p>Donec eleifend, nisl sit amet rhoncus sodales, lacus purus pulvinar metus, id pellentesque ipsum ante a turpis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed quis sapien dolor. Pellentesque suscipit purus felis. Donec felis justo, cursus ut porta imperdiet, posuere eu mi. Fusce interdum augue mauris, quis tincidunt ipsum tincidunt sed. Pellentesque luctus ex leo, id interdum quam consequat eget. Sed eleifend porta convallis. Aenean luctus mauris vitae nulla consectetur placerat. Maecenas auctor sollicitudin nisl, eget efficitur lacus feugiat eu. Nam auctor scelerisque vulputate.</p>
		</div>

	</div>
</template>

<script>
	export default {
		name: 'Type',
		created: function(){
			this.$eventBus.$emit('updateScroll')
		},
		methods: {
			
		}
	}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
	
	.Type {
		padding: 200px 20px;
		max-width: 1500px;
		height: 100vh;
		overflow: scroll;

		.entry {
			margin-bottom: 100px;
		}
	}
	
</style>



// WEBPACK FOOTER //
// src/components/Type.vue