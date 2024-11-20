<script>
	import * as Accordion from '../ui/accordion';

	const customSources = [
		{
			id: '1',
			type: 'copy/paste',
			title: 'Custom Source 1',
			content: 'AI-generated Source content goes here'
		},
		{
			id: '2',
			type: 'webpage',
			title: 'Custom Source 2',
			content: 'Custom Souce content goes here'
		}
	];
</script>

{#each customSources as source (source.id)}
	<Accordion.Item value={source.id} class="border-gray-800">
		<Accordion.Trigger>{source.title}</Accordion.Trigger>
		<Accordion.Content>
			<div class="flex w-full flex-col gap-y-3 p-2 bg-gray-900/70 text-gray-300">
				{source.content}
			</div>
		</Accordion.Content>
	</Accordion.Item>
{/each}
