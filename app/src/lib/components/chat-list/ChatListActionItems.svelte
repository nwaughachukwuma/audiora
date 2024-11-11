<script lang="ts">
	import { goto } from '$app/navigation';
	import { getSessionContext } from '@/stores/sessionContext.svelte';

	export let sessionId: string;

	const { session$ } = getSessionContext();

	async function ongenerate(summary: string) {
		session$.update((session) => {
			if (!session) throw new Error('Session not found');

			session.completed = true;
			session.summary = summary;
			return session;
		});

		return goto(`/audiocast/${sessionId}`, { replaceState: true });
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
