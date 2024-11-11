<script>
	import { cn } from '@/utils/ui.utils';
	import { Button } from '../ui/button';

	export let href;
	export let label = '';
	export let fill = true;
	export let ariaLabel = '';
	let classes = '';
	export { classes as class };
</script>

<Button
	{href}
	target="_blank"
	rel="noopener noreferrer"
	aria-label={ariaLabel}
	class={cn('p-3 h-10 ease-out transition-all hover:bg-inherit', classes)}
>
	<span
		class={cn('w-4 h-4 m-0 text-white align-middle', {
			'fill-current': fill,
			'stroke-current': !fill
		})}
	>
		<slot></slot>
	</span>
	{label}
</Button>
