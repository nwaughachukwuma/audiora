<script lang="ts">
	import { goto } from '$app/navigation';
	import type { ContentCategory } from '@/utils/types';

	export let sessionId: string;
	export let category: ContentCategory;

	function ongenerate(summary: string) {
		console.log('ongenerate', sessionId, summary, category);
		fetch('/api/generate', {
			method: 'POST',
			body: JSON.stringify({ sessionId, summary, category }),
			headers: { 'Content-Type': 'application/json' }
		});
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
