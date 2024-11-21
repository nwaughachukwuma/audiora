<script lang="ts">
	export let content: string;
	$: paragraphs = content.split('\n\n').filter((p) => p.trim());
</script>

<section class="w-full flex flex-col gap-y-3">
	{#each paragraphs as paragraph, idx (idx)}
		<article class="pb-2 border-b leading-relaxed border-b-gray-500/10">
			{paragraph}
		</article>
	{/each}
</section>

<style>
	article :global(code) {
		background-color: rgba(62, 3, 3, 0.1);
		padding: 0.25rem 0.5rem;
		border-radius: 0.25rem;
	}
</style>
