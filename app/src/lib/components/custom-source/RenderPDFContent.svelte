<script lang="ts">
	export let content: string;
	$: paragraphs = content.split('\n').filter((p) => p.trim());
</script>

<article class="prose max-w-full flex flex-col gap-y-3">
	{#each paragraphs as paragraph, idx (idx)}
		{paragraph}
	{/each}
</article>
