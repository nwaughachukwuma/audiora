<div class="relative overflow-hidden w-full flex flex-col h-full">
	<div class="overflow-auto px-10 w-full block h-[calc(86%-2.5rem)]">
		<div class="flex flex-col gap-y-2">
			<h1 class="text-5xl font-bold">🎧 Audiora</h1>
			<h2 class="text-lg">Listen to anything, anytime.</h2>
		</div>

		<slot name="content"></slot>
	</div>

	<div class="h-[14%] fixed px-10 w-[calc(100%-24.5rem)] bottom-0 shrink-0">
		<slot name="chat_box"></slot>
	</div>
</div>
