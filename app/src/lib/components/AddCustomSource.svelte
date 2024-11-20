<script>
	import { cn } from '@/utils/ui.utils';
	export let show = false;
</script>

<div class="container w-full flex justify-center overflow-hidden flex-col items-center" class:show>
	<div>Add Custom Source</div>
</div>

<style>
	.container {
		height: 0;
		opacity: 0;
		transition:
			height 0.3s ease-in-out,
			opacity 0.3s ease-in-out;
	}

	.show {
		opacity: 1;
		height: 10rem;
	}
</style>
