<script lang="ts">
	import { Slider as SliderPrimitive } from 'bits-ui';
	import { cn } from '$lib/utils/ui.utils.js';

	type $$Props = SliderPrimitive.Props & {
		rangeClass?: string;
		thumbClass?: string;
	};

	let className: $$Props['class'] = undefined;
	export let rangeClass: string | undefined = undefined;
	export let thumbClass: string | undefined = undefined;

	export let value: $$Props['value'] = [0];
	export { className as class };
</script>

<SliderPrimitive.Root
	bind:value
	class={cn('relative flex w-full touch-none select-none items-center', className)}
	{...$$restProps}
	let:thumbs
>
	<span class="bg-secondary relative h-2 w-full grow overflow-hidden rounded-full">
		<SliderPrimitive.Range class={cn('bg-primary absolute h-full', rangeClass)} />
	</span>
	{#each thumbs as thumb}
		<SliderPrimitive.Thumb
			{thumb}
			class={cn(
				'border-primary bg-background ring-offset-background focus-visible:ring-ring block h-5 w-5 rounded-full border-2 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
				thumbClass
			)}
		/>
	{/each}
</SliderPrimitive.Root>
