<script lang="ts" context="module">
	export type LinkSources = {
		type: 'link';
		url: string;
	};

	export type CopyPasteSources = {
		type: 'copy/paste';
	};

	export type CustomSources = (LinkSources | CopyPasteSources) & {
		id: string;
		title: string;
		content_type: 'text/plain' | 'text/html' | 'application/pdf';
		content: string;
	};

	const customSources: CustomSources[] = [
		{
			id: '1',
			type: 'copy/paste',
			content_type: 'text/html',
			title: 'Custom Source 1',
			content: 'AI-generated Source content goes here'
		},
		{
			id: '2',
			title: 'Custom Source 2',
			content_type: 'text/plain',
			type: 'link',
			content: 'Custom Souce content goes here',
			url: 'https://www.google.com'
		},
		{
			id: '3',
			type: 'link',
			content_type: 'application/pdf',
			title: 'Custom Source 3',
			content: 'Custom Souce content goes here',
			url: 'https://www.wikipedia.org'
		}
	];
</script>

<script lang="ts">
	import * as Accordion from '../ui/accordion';
	import RenderPdfContent from './RenderPDFContent.svelte';
	export let sources = customSources;
</script>

{#each sources as source (source.id)}
	<Accordion.Item value={source.id} class="border-gray-800">
		<Accordion.Trigger>{source.title}</Accordion.Trigger>
		<Accordion.Content>
			<div class="flex w-full flex-col gap-y-3 p-2 bg-gray-900/70 text-gray-300">
				{#if source.content_type === 'application/pdf'}
					<RenderPdfContent content={source.content} />
				{:else}
					{source.content}
				{/if}
			</div>
		</Accordion.Content>
	</Accordion.Item>
{/each}
