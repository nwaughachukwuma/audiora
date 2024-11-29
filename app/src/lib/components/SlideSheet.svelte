<script>
	import * as Sheet from './ui/sheet';
	import SidebarToggleButton from './SidebarToggleButton.svelte';
	export let open = false;
</script>

<Sheet.Root bind:open closeOnOutsideClick>
	<Sheet.Trigger asChild let:builder>
		<SidebarToggleButton builders={[builder]} />
	</Sheet.Trigger>
	<Sheet.Content side="left" class="bg-gray-900 border-muted">
		<Sheet.Header class="mb-1 text-left">
			<Sheet.Title class="ml-4 text-xl text-gray-200">Audiocasts</Sheet.Title>
		</Sheet.Header>

		<slot />
	</Sheet.Content>
</Sheet.Root>
