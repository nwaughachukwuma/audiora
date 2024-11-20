<script lang="ts">
	import * as Drawer from './ui/drawer';
	import { Button } from './ui/button';
	import * as Accordion from './ui/accordion';
	import { parse } from 'marked';
	import { PlusIcon } from 'lucide-svelte';
	import CustomSources from './CustomSources.svelte';
	import AddCustomSource from './AddCustomSource.svelte';

	export let audioSource: string;

	let snapPoints = [0.75, 0.9];
	let activeSnapPoint = snapPoints[0];
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
				>Audiocast Source
			</Drawer.Title>

			<div class="h-full overflow-hidden overflow-y-auto">
				<div
					class="mx-auto relative w-full h-[calc(100%+120px)] max-w-full px-4 py-2 md:max-w-3xl xl:max-w-4xl"
				>
					<Accordion.Root>
						<Accordion.Item value="item-x" class="border-gray-800 mb-3 rounded-md border">
							<Accordion.Trigger
								class="no-underline hover:no-underline px-3 rounded-md border-dashed bg-gray-900/60 hover:bg-gray-900"
							>
								<span class="capitalize font-medium text-gray-400"> Add custom source </span>
								<span slot="icon" class="p-1 rounded-full border border-gray-500">
									<PlusIcon
										class="inline w-6 h-6 text-gray-400 hover:text-gray-200 transition-all"
									/>
								</span>
							</Accordion.Trigger>
							<Accordion.Content>
								<AddCustomSource show />
							</Accordion.Content>
						</Accordion.Item>

						<Accordion.Item value="item-0" class="border-gray-800">
							<Accordion.Trigger>AI-generated Source</Accordion.Trigger>
							<Accordion.Content>
								<article
									class="prose text-gray-300 flex p-2 flex-col gap-y-3 bg-gray-900/70 text-gray-30"
								>
									{#await parse(audioSource) then parsedContent}
										{@html parsedContent}
									{/await}
								</article>
							</Accordion.Content>
						</Accordion.Item>

						<CustomSources />
					</Accordion.Root>
				</div>
			</div>
		</Drawer.Content>
	</Drawer.Portal>
</Drawer.Root>
