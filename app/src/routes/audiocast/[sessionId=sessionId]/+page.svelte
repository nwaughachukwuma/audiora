<script lang="ts" context="module">
	export type ChatMetadata = {
		source: string;
		transcript: string;
		info?: string;
		title?: string;
	};

	function parseScript(script: string) {
		const matches = [...script.matchAll(/<(Speaker\d+)>(.*?)<\/Speaker\d+>/gs)];
		return matches.map(([, speaker, content]) => `**${speaker}**: ${content}`).join('\n\n');
	}
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { getAnalytics, logEvent } from 'firebase/analytics';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import type { ContentCategory } from '@/utils/types';
	import { env } from '@env';
	import { parse } from 'marked';
	import * as Accordion from '@/components/ui/accordion';
	import RenderMedia from '@/components/RenderMedia.svelte';
	import { page } from '$app/stores';
	import AudiocastPageAction from '@/components/AudiocastPageAction.svelte';
	import AudiocastPageChat from '@/components/AudiocastPageChat.svelte';
	import AudiocastPageSkeletonLoader from '@/components/AudiocastPageSkeletonLoader.svelte';
	import RenderAudioSources from '@/components/RenderAudioSources.svelte';
	import AudiocastPageHeader from '@/components/AudiocastPageHeader.svelte';
	import { toast } from 'svelte-sonner';

	export let data;

	const { session$, sessionModel$ } = getSessionContext();

	let generating = false;

	$: sessionId = $page.params.sessionId;
	$: sessionModel = $sessionModel$ || data.sessionModel;
	$: checkAudiocast(sessionId);

	$: sessionTitle = sessionModel.metadata?.title || 'Untitled';
	$: isGenerating = sessionModel.status === 'generating' || generating;

	async function generateAudiocast(sessionId: string, category: ContentCategory, summary: string) {
		generating = true;
		return fetch(`${env.API_BASE_URL}/audiocast/generate`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, summary, category }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<string>((res) => {
				if (res.ok) return res.json();
				throw new Error(res.statusText);
			})
			.then(() => toast.success('Audiocast generated successfully'));
	}

	async function checkAudiocast(sessionId: string) {
		if (isGenerating || sessionModel.status === 'completed') return;

		return fetch(`${env.API_BASE_URL}/audiocast/${sessionId}`)
			.then((res) => {
				if (res.ok) return;
				else if (res.status === 404 && $session$?.summary) {
					return generateAudiocast(sessionId, sessionModel.category, $session$.summary);
				}
				throw new Error(res.statusText);
			})
			.catch((error) => {
				toast.error('Error fetching audiocast:', { description: String(error) });
			})
			.finally(() => (generating = false));
	}

	onMount(() => {
		logEvent(getAnalytics(), 'page_view', {
			page_title: 'Audiocast',
			page_path: `/audiocast/${sessionId}`
		});
	});
</script>

<div
	class="mx-auto sm:max-w-xl lg:max-w-3xl max-w-full flex h-full w-full pb-40 overflow-auto flex-col items-center max-sm:px-4"
>
	<AudiocastPageHeader category={sessionModel.category} title={sessionModel.metadata?.title} />

	{#if sessionModel.status === 'completed'}
		<div class="flex w-full mt-4 flex-col gap-y-3">
			<RenderMedia filename={sessionId} let:uri>
				<audio controls class="w-full animate-fade-in block">
					<source src={uri} type="audio/mpeg" />
					Your browser does not support the audio element.
				</audio>
			</RenderMedia>

			<Accordion.Root>
				{#if sessionModel.metadata?.transcript}
					<Accordion.Item value="item-1" class="border-gray-800">
						<Accordion.Trigger>Audio Transcript</Accordion.Trigger>
						<Accordion.Content>
							<article
								class="flex max-h-96 overflow-y-auto w-full flex-col gap-y-3 p-2 bg-gray-900/70 text-gray-300"
							>
								{#await parse(parseScript(sessionModel.metadata.transcript)) then parsedContent}
									{@html parsedContent}
								{/await}
							</article>
						</Accordion.Content>
					</Accordion.Item>
				{/if}

				{#if sessionModel.metadata?.source}
					<RenderAudioSources aiSource={sessionModel.metadata.source} />
				{/if}

				<Accordion.Item value="item-0" class="border-gray-800">
					<Accordion.Trigger>Show Waveform</Accordion.Trigger>
					<Accordion.Content>
						<RenderMedia filename="{sessionId}.mp4" let:uri>
							<video controls class="w-full h-64 animate-fade-in block">
								<source src={uri} type="video/mp4" />
								Your browser does not support the video element.

								<track kind="captions" />
							</video>
						</RenderMedia>
					</Accordion.Content>
				</Accordion.Item>
			</Accordion.Root>

			<AudiocastPageAction {sessionId} {sessionTitle} on:showChats>
				<AudiocastPageChat slot="chats-button" chats={sessionModel.chats} />
			</AudiocastPageAction>
		</div>
	{:else}
		<div class="flex flex-col w-full">
			<AudiocastPageSkeletonLoader />

			{#if isGenerating}
				<div class="flex mt-4 flex-col gap-y-3 w-full items-center">
					<p class="py-2 px-4 bg-sky-600/20 animate-pulse text-sky-300 rounded-sm">
						Generating your audiocast...Please wait
					</p>

					{#if sessionModel?.metadata?.info}
						<p class="py-2 px-4 animate-pulse text-gray-400 rounded-sm">
							Status: {sessionModel.metadata.info}
						</p>
					{/if}
				</div>
			{/if}
		</div>
	{/if}
</div>

<style lang="postcss">
	article :global(p) {
		@apply text-sm;
	}
</style>
