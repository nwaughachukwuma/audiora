<script lang="ts" context="module">
	type GenerateAudiocastResponse = {
		url: string;
		script: string;
		source_content: string;
		created_at?: string;
	};
</script>

<script lang="ts">
	import Spinner from '@/components/Spinner.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';

	const { session$ } = getSessionContext();

	let generating = false;

	async function generateAudiocast(sessionId: string, category: ContentCategory, summary: string) {
		if (generating) return;
		generating = true;

		// return fetch(`${env.API_BASE_URL}/audiocast/generate`, {
		// 	method: 'POST',
		// 	body: JSON.stringify({ sessionId, summary, category }),
		// 	headers: { 'Content-Type': 'application/json' }
		// })
		// 	.then<GenerateAudiocastResponse>((res) => {
		// 		if (res.ok) return res.json();
		// 		throw new Error('Failed to generate audiocast');
		// 	})
		// 	.finally(() => (generating = false));
	}
</script>

{#if !$session$?.summary}
	<Spinner />
{:else}
	{@const { summary, category } = $session$}
	{#await generateAudiocast($session$.id, category, summary)}
		<Spinner />
	{:then data}
		<pre>
			{JSON.stringify(data, null, 2)}
		</pre>
	{:catch error}
		<div>{String(error)}</div>
	{/await}
{/if}
