<script lang="ts" context="module">
	type GenerateAudiocastResponse = {
		url: string;
		script: string;
		source_content: string;
		created_at?: string;
	};
</script>

<script lang="ts">
	import { goto } from '$app/navigation';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';

	export let sessionId: string;
	export let category: ContentCategory;
	export let generating = false;

	async function ongenerate(summary: string) {
		if (generating) return;

		generating = true;

		return fetch(`${env.API_BASE_URL}/audiocast/generate`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, summary, category }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<GenerateAudiocastResponse>((res) => {
				if (res.ok) res.json();
				throw new Error('Failed to generate audiocast');
			})
			.finally(() => (generating = false));
	}

	function onreviewSource() {
		console.log('reviewSource');
	}

	async function onstartNew() {
		return goto('/', { invalidateAll: true, replaceState: true });
	}
</script>

<div>
	<slot {ongenerate} {onreviewSource} {onstartNew}></slot>
</div>
