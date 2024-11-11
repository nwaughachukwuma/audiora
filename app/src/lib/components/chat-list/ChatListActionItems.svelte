<script lang="ts">
	import { goto } from '$app/navigation';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';

	export let sessionId: string;

	const { session$, audioSource$, fetchingSource$ } = getSessionContext();

	async function ongenerate(summary: string) {
		session$.update((session) => {
			if (!session) throw new Error('Session not found');

			session.completed = true;
			session.summary = summary;
			return session;
		});

		return goto(`/audiocast/${sessionId}`, { replaceState: true });
	}

	async function onreviewSource(category: ContentCategory, summary: string) {
		if ($fetchingSource$) return;
		$fetchingSource$ = true;

		const response = await fetch(`${env.API_BASE_URL}/get-audiocast-source`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, category, summary }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<string>((res) => {
				if (res.ok) return res.json();
				throw new Error('Failed to get audiocast source');
			})
			.finally(() => ($fetchingSource$ = false));

		$audioSource$ = response;
	}

	async function onstartNew() {
		return goto('/', { invalidateAll: true, replaceState: true });
	}
</script>

<div>
	<slot {ongenerate} {onreviewSource} {onstartNew}></slot>
</div>
