<script lang="ts">
	import { goto } from '$app/navigation';
	import { Button } from '@/components/ui/button';
	import ShareModal from './share/ShareModal.svelte';
	import { getShareableLink, getShareTitle } from '@/utils/shareMeta';
	import { Share2Icon } from 'lucide-svelte';

	export let sessionId: string;
	export let sessionTitle: string;

	$: shareableLink = getShareableLink(sessionId);
	$: shareTitle = getShareTitle(sessionTitle);
</script>

<div class="mt-3 w-full items-center justify-center gap-3 grid grid-cols-2 sm:grid-cols-2">
	<ShareModal url={shareableLink} title={shareTitle}>
		<Button
			slot="trigger"
			variant="ghost"
			class="py-6 w-full text-base rounded-md no-underline hover:no-underline bg-gray-800 text-gray-200 hover:bg-gray-700"
			on:click
		>
			<span> Share </span>
			<Share2Icon class="w-4 h-4 ml-2 inline" />
		</Button>
	</ShareModal>

	<Button
		on:click={() => goto('/', { invalidateAll: true, replaceState: true })}
		class="py-6 rounded-md text-base no-underline text-center hover:no-underline bg-emerald-600 text-emerald-100 hover:bg-emerald-700"
		>Create Audiocast
	</Button>
</div>
