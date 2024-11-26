<script>
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import { Button } from '@/components/ui/button';
	const { session$, sessionModel$ } = getSessionContext();

	$: $sessionModel$;
</script>

<!-- TODO: Use only the DB references -->
{#if $session$ && !$session$.completed}
	<div
		class="w-full mx-auto px-4 md:max-w-xl h-full flex flex-col gap-3 items-center justify-center"
	>
		<p>
			You've not completed specifying your content preferences. Please complete the chat session to
			generate an audiocast.
		</p>
		<Button
			href="/chat/{$session$.id}"
			class="text-blue-500 px-16 no-underline hover:no-underline bg-gray-800 hover:bg-gray-700"
			>Generate Audiocast</Button
		>
	</div>
{:else}
	<slot />
{/if}
