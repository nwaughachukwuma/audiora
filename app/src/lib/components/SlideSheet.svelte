<script>
	import * as Sheet from './ui/sheet';
	import { Button } from './ui/button';
	export let open = false;
</script>

<Sheet.Root bind:open closeOnOutsideClick>
	<Sheet.Trigger asChild let:builder>
		<Button builders={[builder]} variant="ghost" class="px-2">
			<svg viewBox="0 0 24 24" fill="none" class="text-icon-secondary h-6">
				<path
					fill="currentColor"
					fill-rule="evenodd"
					clip-rule="evenodd"
					d="M2 6C2 5.44772 2.44772 5 3 5H21C21.5523 5 22 5.44772 22 6C22 6.55228 21.5523 7 21 7H3C2.44772 7 2 6.55228 2 6ZM2 12C2 11.4477 2.44772 11 3 11H21C21.5523 11 22 11.4477 22 12C22 12.5523 21.5523 13 21 13H3C2.44772 13 2 12.5523 2 12ZM2 18C2 17.4477 2.44772 17 3 17H11C11.5523 17 12 17.4477 12 18C12 18.5523 11.5523 19 11 19H3C2.44772 19 2 18.5523 2 18Z"
				></path>
			</svg>
		</Button>
	</Sheet.Trigger>
	<Sheet.Content side="left" class="bg-gray-900 border-muted">
		<Sheet.Header class="mb-1 text-left">
			<Sheet.Title class="ml-4 text-gray-200">Audiocasts</Sheet.Title>
		</Sheet.Header>

		<slot />
	</Sheet.Content>
</Sheet.Root>
