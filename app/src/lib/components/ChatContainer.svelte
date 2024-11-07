<div class="relative overflow-hidden w-full flex flex-col h-full">
	<div class="overflow-auto px-10 w-full block h-[calc(85%-2.5rem)]">
		<div class="flex flex-col gap-y-2">
			<h1 class="text-5xl font-bold">🎧 Audiora</h1>
			<h2 class="text-lg">Listen to anything, anytime.</h2>
		</div>

		<slot name="content"></slot>
	</div>

	<div class="h-[16%] fixed w-[calc(100%-24.5rem)] bottom-0 shrink-0">
		<slot name="chat_input"></slot>
	</div>
</div>
