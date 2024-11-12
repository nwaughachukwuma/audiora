<div class="w-full max-w-3xl mx-auto p-6">
	<!-- {/* Title skeleton */} -->
	<div class="h-8 w-48 bg-gray-800 rounded animate-pulse mb-8" />

	<!-- {/* Player container */} -->
	<div class="w-full rounded-lg bg-gray-800 p-4 mb-6">
		<!-- {/* Player controls and progress row */} -->
		<div class="flex items-center gap-4 mb-2">
			<!-- {/* Play button skeleton */} -->
			<div class="w-8 h-8 rounded-full bg-gray-700 animate-pulse" />

			<!-- {/* Progress bar skeleton */} -->
			<div class="flex-1 h-2 bg-gray-700 rounded animate-pulse" />

			<!-- {/* Volume and menu buttons skeleton */} -->
			<div class="flex gap-2">
				<div class="w-8 h-8 rounded bg-gray-700 animate-pulse" />
				<div class="w-8 h-8 rounded bg-gray-700 animate-pulse" />
			</div>
		</div>
	</div>

	{#each Array(3).fill(0) as _, index (index)}
		<div class="mb-4">
			<div class="flex items-center justify-between p-4 border-b border-gray-800">
				<div class="h-6 w-32 bg-gray-800 rounded animate-pulse" />
				<div class="w-6 h-6 bg-gray-800 rounded animate-pulse" />
			</div>
		</div>
	{/each}

	<div class="flex gap-4 mt-6">
		<div class="w-12 h-12 bg-gray-800 rounded animate-pulse" />
		<div class="w-12 h-12 bg-gray-800 rounded animate-pulse" />
		<div class="w-40 h-12 bg-gray-800 rounded animate-pulse" />
	</div>
</div>
