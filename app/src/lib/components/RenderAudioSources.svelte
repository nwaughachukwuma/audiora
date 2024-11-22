<script lang="ts">
	import { parse } from 'marked';
	import * as Accordion from './ui/accordion';
	import CustomSources from './custom-source/CustomSources.svelte';

	export let aiSource: string;
</script>

<render-audio-sources>
	<Accordion.Item value="ai-source-item" class="border-gray-800">
		<Accordion.Trigger>AI-generated Source</Accordion.Trigger>
		<Accordion.Content>
			<article
				class="prose leading-relaxed max-h-96 overflow-y-auto text-gray-300 flex p-2 flex-col gap-y-3 bg-gray-900/70 text-gray-30"
			>
				{#await parse(aiSource) then parsedContent}
					{@html parsedContent}
				{/await}
			</article>
		</Accordion.Content>
	</Accordion.Item>

	<CustomSources />
</render-audio-sources>

<style lang="postcss">
	article :global(p) {
		@apply text-sm;
	}
</style>
