<script context="module">
	export const FINAL_RESPONSE_PREFIX = 'Ok, thanks for clarifying!';
	export const FINAL_RESPONSE_SUFFIX =
		'Please click the button below to start generating the audiocast.';
</script>

<script lang="ts">
	import { goto } from '$app/navigation';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';
	import { toast } from 'svelte-sonner';
	import { Button } from './ui/button';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import RenderAudioSource from '@/components/RenderAudioSource.svelte';
	import { streamingResponse } from '@/utils/streamingResponse';

	export let sessionId: string;
	export let category: ContentCategory;
	export let content: string;
	export let title: string;

	const { session$, audioSource$, fetchingSource$, sessionId$, sessionCompleted$ } =
		getSessionContext();

	function getSummary() {
		const replacePrefixRegex = new RegExp(FINAL_RESPONSE_PREFIX, 'gi');
		const replaceSuffixRegex = new RegExp(FINAL_RESPONSE_SUFFIX, 'gi');
		return content.replace(replacePrefixRegex, '').replace(replaceSuffixRegex, '').trim();
	}

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

		return fetch(`${env.API_BASE_URL}/get-audiocast-source`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, category, summary }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<string>((res) => {
				if (res.ok) return res.json();
				throw new Error('Failed to get audiocast source');
			})
			.then((res) => {
				$audioSource$ = res;
				toast.success('Audiocast source generated successfully');
			})
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
				summary: getSummary()
			}),
			headers: { 'Content-Type': 'application/json' }
		})
			.then(handleStreamingResponse)
			.finally(() => (generatingTitle = false));
	}

	async function handleStreamingResponse(res: Response) {
		if (!res.ok) return;

		for await (const chunk of streamingResponse(res)) {
			session$.update((session) => {
				if (session) {
					if (session.title.toLowerCase() === 'untitled') session.title = '';
					session.title += chunk;
				}
				return session;
			});
		}
	}
</script>

<div>
	{#if $sessionCompleted$}
		<div class="mt-3 w-full items-center justify-center flex">
			<a
				href="/audiocast/{$sessionId$}"
				data-sveltekit-preload-data="hover"
				class="py-3 rounded-md px-16 no-underline hover:no-underline bg-emerald-600 text-emerald-100 hover:bg-emerald-700"
				>View Audiocast</a
			>
		</div>
	{:else}
		<div class="animate-fade-in grid sm:grid-cols-2 gap-3">
			<Button
				class="bg-emerald-600 text-emerald-100 hover:bg-emerald-700"
				on:click={() => ongenerate(getSummary())}>Generate Audiocast</Button
			>

			{#if $audioSource$}
				<RenderAudioSource audioSource={$audioSource$} />
			{:else}
				<Button
					variant="ghost"
					class="bg-gray-800 hover:bg-gray-700 text-emerald-600 hover:text-emerald-600"
					on:click={() => onreviewSource(category, getSummary())}
				>
					Review Source
				</Button>
			{/if}
		</div>
	{/if}
</div>
