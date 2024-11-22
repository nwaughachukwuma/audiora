<script lang="ts">
	import * as Accordion from '../ui/accordion';
	import RenderWebContent from './RenderWebContent.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte';

	const { customSources$ } = getSessionContext();

	$: customSources = $customSources$?.sort((a, b) => {
		if (a.created_at && b.created_at) {
			return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
		}
		return 0;
	});

	function truncate(str: string, n: number) {
		return str.length > n ? str.substring(0, n - 1) + '...' : str;
	}
</script>

{#if customSources == null}
	<div class="flex flex-col gap-y-0.5 pt-0.5 w-full">
		<div class="h-14 w-full bg-gray-800 animate-pulse" />
		<div class="h-14 w-full bg-gray-800 animate-pulse" />
	</div>
{:else}
	{#each customSources as source, idx (source.id)}
		<Accordion.Item value={source.id} class="border-gray-800">
			<Accordion.Trigger>
				<div class="inline-flex break-words text-wrap">
					<span class="shrink-0 inline-flex">
						Custom Source {idx + 1}
					</span>
					{#if source.source_type === 'link'}
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
{/if}
