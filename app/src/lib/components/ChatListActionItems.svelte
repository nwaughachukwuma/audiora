<script lang="ts">
	import { goto } from '$app/navigation';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';
	import { toast } from 'svelte-sonner';
	import { Button } from './ui/button';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import { streamingResponse } from '@/utils/streamingResponse';
	import { Share2Icon } from 'lucide-svelte';
	import ShareModal from './share/ShareModal.svelte';
	import { getShareableLink, getShareTitle } from '@/utils/shareMeta';
	import ManageAudioSourceDrawer from './ManageAudioSourceDrawer.svelte';

	export let sessionId: string;
	export let category: ContentCategory;
	export let summary: string;
	export let title: string;

	const {
		session$,
		audioSource$,
		fetchingSource$,
		sessionId$,
		sessionCompleted$,
		updateSessionTitle
	} = getSessionContext();

	async function ongenerate(summary: string) {
		session$.update((session) => {
			if (!session) throw new Error('Session not found');
			session.summary = summary;
			return session;
		});

		return goto(`/audiocast/${sessionId}`, { replaceState: true }).then(() => {
			session$.update((session) => {
				if (!session) throw new Error('Session not found');
				session.completed = true;
				return session;
			});
		});
	}

	async function onreviewSource(category: ContentCategory, summary: string) {
		if ($fetchingSource$) return;
		$fetchingSource$ = true;

		return fetch(`${env.API_BASE_URL}/generate-aisource`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, category, preferenceSummary: summary }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<string>((res) => {
				if (res.ok) return res.json();
				throw new Error('Failed to get audiocast source');
			})
			.then(() => toast.success('AI-generated source material generated successfully'))
			.catch((error) => toast.error(error.message))
			.finally(() => ($fetchingSource$ = false));
	}

	$: if (title.toLowerCase() === 'untitled') getSessionTitle();

	let generatingTitle = false;

	async function getSessionTitle() {
		if (generatingTitle) return;
		generatingTitle = true;

		return fetch(`${env.API_BASE_URL}/get-session-title`, {
			method: 'POST',
			body: JSON.stringify({
				sessionId,
				category,
				summary
			}),
			headers: { 'Content-Type': 'application/json' }
		})
			.then(handleStreamingResponse)
			.finally(() => (generatingTitle = false));
	}

	async function handleStreamingResponse(res: Response) {
		if (!res.ok) return;

		for await (const chunk of streamingResponse(res)) {
			updateSessionTitle(chunk);
		}
	}

	$: shareableLink = getShareableLink(sessionId);
	$: shareTitle = getShareTitle(title);
</script>

<div>
	{#if $sessionCompleted$}
		<div class="mt-3 w-full items-center justify-center gap-3 grid grid-cols-2 sm:grid-cols-2">
			<Button
				href="/audiocast/{$sessionId$}"
				data-sveltekit-preload-data="hover"
				class="py-6 rounded-md text-base no-underline text-center hover:no-underline bg-emerald-600 text-emerald-100 hover:bg-emerald-700"
				>View Audiocast</Button
			>

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
		</div>
	{:else}
		<div class="animate-fade-in grid sm:grid-cols-2 gap-3">
			<Button
				class="bg-emerald-600 text-emerald-100 text-base py-6 hover:bg-emerald-700"
				on:click={() => ongenerate(summary)}>Generate Audiocast</Button
			>

			<ManageAudioSourceDrawer
				aiSource={$audioSource$}
				on:click={() => {
					if (!$audioSource$ && !$fetchingSource$) {
						onreviewSource(category, summary);
					}
				}}
			/>
		</div>
	{/if}
</div>
