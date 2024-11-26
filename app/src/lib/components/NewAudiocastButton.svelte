<script>
	import { goto } from '$app/navigation';
	import { PlusIcon } from 'lucide-svelte';
	import { Button } from './ui/button';
</script>

<Button
	on:click={() => goto('/', { invalidateAll: true, replaceState: true })}
	class="py-6 px-10 animate-fade-in rounded-md text-base no-underline text-center hover:no-underline bg-gray-800 text-gray-200 hover:bg-gray-700"
>
	<PlusIcon class="w-4 h-4 inline mr-2" />
	New Audiocast
</Button>
