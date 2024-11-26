<script lang="ts">
	import { Button } from '@/components/ui/button';
	import ShareModal from './share/ShareModal.svelte';
	import { getShareableLink, getShareTitle } from '@/utils/shareMeta';
	import { Share2Icon } from 'lucide-svelte';
	import NewAudiocastButton from './NewAudiocastButton.svelte';

	export let sessionId: string;
	export let sessionTitle: string;

	$: shareableLink = getShareableLink(sessionId);
	$: shareTitle = getShareTitle(sessionTitle);
</script>

<div class="mt-3 items-center gap-3 flex w-fit">
	<slot name="chats-button" />

	<ShareModal url={shareableLink} title={shareTitle}>
		<Button
			slot="trigger"
			variant="ghost"
			class="py-6 w-16 text-base rounded-md no-underline hover:no-underline bg-gray-800 text-gray-200 hover:bg-gray-700"
			on:click
		>
			<Share2Icon class="w-4 inline" />
		</Button>
	</ShareModal>

	<NewAudiocastButton />
</div>
