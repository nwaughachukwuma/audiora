<script>
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import { Button } from '@/components/ui/button';
	import { goto } from '$app/navigation';

	const { session$ } = getSessionContext();
</script>

{#if !$session$}
	<div>Session not found</div>
	<Button
		on:click={() => {
			goto('/', { invalidateAll: true, replaceState: true });
		}}
		class="text-blue-500"
	>
		Return home
	</Button>
{:else if $session$.completed && $session$.summary}
	<slot />
{:else}
	<div>
		You've not completed specifying your content preferences. Please complete the chat session to
		generate an audiocast.

		<a href="/chat/{$session$.id}" class="text-blue-500">Generate Audiocast</a>
	</div>
{/if}
