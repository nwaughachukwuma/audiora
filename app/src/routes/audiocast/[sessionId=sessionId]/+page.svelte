<script lang="ts" context="module">
	export type ChatMetadata = {
		source: string;
		transcript: string;
		info?: string;
		title?: string;
	};

	type GenerateAudiocastResponse = {
		script: string;
		source_content: string;
		created_at?: string;
	};

	function parseScript(script: string) {
		const matches = [...script.matchAll(/<(Speaker\d+)>(.*?)<\/Speaker\d+>/gs)];
		return matches.map(([, speaker, content]) => `**${speaker}**: ${content}`).join('\n\n');
	}
</script>

<script lang="ts">
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

	const { customSources$, session$, sessionModel$ } = getSessionContext();

	let generating = false;

	$: sessionId = $page.params.sessionId;
	$: sessionModel = $sessionModel$;
	$: $customSources$;

	$: $customSources$;

	async function generateAudiocast(sessionId: string, category: ContentCategory, summary: string) {
		if (generating) return;
		generating = true;

		return fetch(`${env.API_BASE_URL}/audiocast/generate`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, summary, category }),
			headers: { 'Content-Type': 'application/json' }
		})
			.then<GenerateAudiocastResponse>((res) => {
				if (res.ok) return res.json();
				throw new Error('Failed to generate audiocast');
			})
			.finally(() => (generating = false));
	}

	async function getAudiocast(sessionId: string) {
		return fetch(`${env.API_BASE_URL}/audiocast/${sessionId}`).then<GenerateAudiocastResponse>(
			(res) => {
				if (res.status === 404 && $session$?.summary) {
					const { summary, category } = $session$;
					return generateAudiocast(sessionId, category, summary);
				} else if (res.ok) return res.json();

				throw new Error('Failed to get audiocast');
			}
		);
	}
</script>

<div class="mx-auto flex h-full w-full pb-40 overflow-auto mt-6 flex-col items-center px-2 sm:px-1">
	{#if sessionModel}
		<AudiocastPageHeader session={sessionModel} />
	{/if}

	{#await getAudiocast(sessionId)}
		<div class="flex flex-col w-full items-center justify-center -mt-6">
			<AudiocastPageSkeletonLoader />

			{#if generating}
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
	{:then data}
		<div class="flex w-full px-4 flex-col gap-y-3 sm:max-w-xl lg:max-w-3xl max-w-full">
			<RenderMedia filename={sessionId} let:uri>
				<audio controls class="w-full animate-fade-in block">
					<source src={uri} type="audio/mpeg" />
					Your browser does not support the audio element.
				</audio>
			</RenderMedia>

			<Accordion.Root>
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

				<Accordion.Item value="item-1" class="border-gray-800">
					<Accordion.Trigger>Audio Transcript</Accordion.Trigger>
					<Accordion.Content>
						<article
							class="flex max-h-96 overflow-y-auto w-full flex-col gap-y-3 p-2 bg-gray-900/70 text-gray-300"
						>
							{#await parse(parseScript(data.script)) then parsedContent}
								{@html parsedContent}
							{/await}
						</article>
					</Accordion.Content>
				</Accordion.Item>

				<RenderAudioSources aiSource={data.source_content} />
			</Accordion.Root>

			{#if sessionModel}
				{@const sessionTitle = sessionModel.metadata?.title || 'Untitled'}
				<AudiocastPageAction {sessionId} {sessionTitle} on:showChats>
					<AudiocastPageChat slot="chats-button" chats={sessionModel.chats} />
				</AudiocastPageAction>
			{/if}
		</div>
	{:catch error}
		<div>Error: {String(error)}</div>
	{/await}
</div>

<style lang="postcss">
	article :global(p) {
		@apply text-sm;
	}
</style>
