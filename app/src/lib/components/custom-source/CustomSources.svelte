<script lang="ts">
	import { getCustomSources } from '@/stores/customSources.svelte';
	import * as Accordion from '../ui/accordion';
	import RenderWebContent from './RenderWebContent.svelte';

	const { sources$ } = getCustomSources();

	$: sources = $sources$;

	function truncate(str: string, n: number) {
		return str.length > n ? str.substring(0, n - 1) + '...' : str;
	}
</script>

{#each sources as source, idx (source.id)}
	<Accordion.Item value={source.id} class="border-gray-800">
		<Accordion.Trigger>
			<div class="inline-flex break-words text-wrap">
				<span class="shrink-0 inline-flex">
					Custom Source {idx + 1}
				</span>
				{#if source.type === 'link'}
					{':'}
					<span class="text-gray-400 text-start ml-1">
						{truncate(source.url, 45)}
					</span>
				{/if}
			</div>
		</Accordion.Trigger>
		<Accordion.Content>
			<div
				class="flex w-full max-h-96 overflow-y-auto flex-col gap-y-3 p-2 bg-gray-900/70 text-gray-300"
			>
				<RenderWebContent content={source.content} />
			</div>
		</Accordion.Content>
	</Accordion.Item>
{/each}
