<script lang="ts">
	import * as Drawer from './ui/drawer';
	import { Button } from './ui/button';
	import * as Accordion from './ui/accordion';
	import { PlusIcon } from 'lucide-svelte';
	import AddCustomSource from './custom-source/AddCustomSource.svelte';
	import { env } from '@env';
	import RenderAudioSources from './RenderAudioSources.svelte';
	import { getSessionContext } from '@/stores/sessionContext.svelte';
	import { toast } from 'svelte-sonner';

	export let aiSource: string;

	const { sessionId$ } = getSessionContext();

	let snapPoints = [0.75, 0.95];
	let activeSnapPoint = snapPoints[0];
	let generatingSource = false;

	let accordionResetKey = {};

	$: sessionId = $sessionId$;

	function accordionValueChanged(v: string | string[] | undefined) {
		if (v === 'item-x') {
			activeSnapPoint = snapPoints[snapPoints.length - 1];
		}
	}

	async function createSourceContent(endpoint: string, data: Record<string, any>) {
		if (generatingSource) return;
		generatingSource = true;

		return fetch(`${env.API_BASE_URL}/${endpoint}`, {
			method: 'POST',
			body: JSON.stringify(data),
			headers: { 'Content-Type': 'application/json' }
		})
			.then((res) => {
				if (res.ok) return res.json();
				throw new Error('Failed to fetch');
			})
			.then(() => toast.success('Custom source added successfully'))
			.catch((e) => {
				console.error(e);
				toast.error('Failed to add custom source', { description: e.message });
			})
			.finally(() => {
				generatingSource = false;
				accordionResetKey = {};
			});
	}

	async function createURLContent(url: string) {
		return createSourceContent('generate-custom-source', { url, sessionId });
	}

	async function createCopyPasteContent(text: string) {
		return createSourceContent('save-copied-source', { text, sessionId });
	}
</script>

<Drawer.Root {snapPoints} bind:activeSnapPoint direction="bottom" dismissible shouldScaleBackground>
	<Drawer.Trigger>
		<Button variant="ghost" class="bg-gray-800 text-base py-6 w-full hover:bg-gray-700 text-white"
			>Manage Audiocast Sources
		</Button>
	</Drawer.Trigger>

	<Drawer.Overlay class="bg-black/40" />

	<Drawer.Portal>
		<Drawer.Content class="border-neutral-800 pb-40 block h-full w-full rounded-t-md">
			<Drawer.Title
				class="text-2xl px-4 py-2 mx-auto md:max-w-3xl xl:max-w-4xl w-full gradient-gray-to-emerald font-medium"
			>
				Audiocast Source
			</Drawer.Title>

			<div class="h-full overflow-hidden overflow-y-auto">
				<div
					class="mx-auto relative w-full h-[calc(100%+120px)] max-w-full px-4 py-2 md:max-w-3xl xl:max-w-4xl"
				>
					{#key accordionResetKey}
						<Accordion.Root onValueChange={accordionValueChanged}>
							<Accordion.Item value="item-x" class="mb-3 rounded-md border-none">
								<Accordion.Trigger
									class="no-underline hover:no-underline px-3 border-gray-700 rounded-md border border-dashed bg-gray-900/60 hover:bg-gray-900"
								>
									<span class="capitalize font-medium text-gray-400"> Add custom source </span>
									<span slot="icon" class="p-1 rounded-full border border-gray-500">
										<PlusIcon
											class="inline w-6 h-6 text-gray-400 hover:text-gray-200 transition-all"
										/>
									</span>
								</Accordion.Trigger>
								<Accordion.Content class="accordion-content">
									<AddCustomSource
										{generatingSource}
										on:submitURL={({ detail }) => createURLContent(detail.url)}
										on:submitCopyPaste={({ detail }) => createCopyPasteContent(detail.text)}
									/>
								</Accordion.Content>
							</Accordion.Item>

							<RenderAudioSources {aiSource} />
						</Accordion.Root>
					{/key}
				</div>
			</div>
		</Drawer.Content>
	</Drawer.Portal>
</Drawer.Root>

<style>
	:global(.accordion-content div) {
		padding-bottom: 4px;
		max-height: 100%;
	}
</style>
