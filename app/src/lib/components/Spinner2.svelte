<script lang="ts" context="module">
	export type SpinnerSize = 'small' | 'medium' | 'large';
	const sizeClasses: Record<SpinnerSize, string> = {
		small: 'w-4 h-4',
		medium: 'w-6 h-6',
		large: 'w-10 h-10'
	};
</script>

<script lang="ts">
	export let size: SpinnerSize = 'medium';
	export let color = 'text-gray-600';
</script>

<div class="flex w-full h-full justify-center items-center">
	<div class={`${sizeClasses[size]} ${color}`}>
		<svg class="animate-spin" viewBox="0 0 24 24">
			<path
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				d="M12 2C6.477 2 2 6.477 2 12c0 1.821.487 3.53 1.338 5"
			/>
		</svg>
	</div>
</div>

<style>
	.animate-spin {
		animation-duration: 0.5s;
	}
</style>
