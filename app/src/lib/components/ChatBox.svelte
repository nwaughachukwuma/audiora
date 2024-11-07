<script lang="ts" context="module">
	import { debounce } from 'throttle-debounce';

	export const updateCursor = debounce(200, (field: HTMLElement, autofocus = false) => {
		const sel = window.getSelection();
		if (!sel || !field.childNodes.length) return;

		const range = document.createRange();
		range.setStart(field.childNodes[0], field.innerText.length);
		range.setEnd(field.childNodes[0], field.innerText.length);

		sel.removeAllRanges();
		sel.addRange(range);

		if (autofocus) field.focus();
	});
</script>

<script lang="ts">
	import { createEventDispatcher, tick } from 'svelte';
	import cs from 'clsx';

	export let searchTerm = '';
	export let autofocus = true;
	export let showIcon = true;
	export let placeholder = '';
	export let disabled = false;
	export let iconPosition: 'left' | 'right' = 'right';
	export let submitOnBlur = false;

	export function hasFocus() {
		return document.activeElement === inputEl;
	}

	export function setFocus() {
		tick().then(() => inputEl?.focus());
	}

	const dispatch = createEventDispatcher<{ keypress: void }>();

	let inputEl: HTMLDivElement | undefined;

	$: autofocus && setFocus();

	$: placeholder = searchTerm ? '' : placeholder;

	$: if (inputEl && searchTerm) {
		inputEl.removeAttribute('data-placeholder');
	} else if (inputEl) {
		inputEl.setAttribute('data-placeholder', placeholder);
	}

	$: inputEl && updateCursor(inputEl, autofocus);

	function handleKeyPress(ev: KeyboardEvent) {
		if (ev.key === 'Enter' && !ev.shiftKey && searchTerm) {
			ev.preventDefault();
			dispatch('keypress');
		}
	}

	function onInput() {
		if (!inputEl) return;
		if (inputEl.innerHTML.trim() === '<br>') {
			inputEl.innerHTML = '';
		}
	}
</script>

<div
	class="relative flex min-h-14 w-full gap-x-2 rounded-md border-2 border-zinc-500 p-1 pl-2.5 focus-within:border-emerald-600"
>
	{#if showIcon && iconPosition === 'left'}
		<slot name="icon-left" {disabled} />
	{/if}

	<div class="flex w-[90%] overflow-y-auto overflow-x-hidden pl-0.5 pr-0 pt-2 outline-none">
		<div
			id="contentDiv"
			role="textbox"
			tabindex="0"
			contenteditable
			class={cs(
				'peer block h-full w-full break-words border-none bg-transparent text-left text-[16px] outline-none',
				{ 'pointer-events-none': disabled }
			)}
			data-placeholder={placeholder}
			spellcheck={false}
			bind:this={inputEl}
			bind:textContent={searchTerm}
			on:keypress={handleKeyPress}
			on:blur={() => submitOnBlur && dispatch('keypress')}
			on:input={onInput}
		/>
	</div>
	<div class:hidden={!$$slots['icon-right']} class="absolute bottom-0 right-0 flex h-full pr-2">
		{#if showIcon && iconPosition === 'right'}
			<span class="self-end">
				<slot name="icon-right" {disabled} />
			</span>
		{/if}
	</div>
</div>

<style lang="postcss">
	#contentDiv[data-placeholder]::before {
		content: attr(data-placeholder);
		color: rgba(var(--fg));
		opacity: 0.6;
		font-size: 16px;
		pointer-events: none;
		display: inline-block;
	}

	#contentDiv[data-placeholder]::before {
		@apply bg-gradient-to-r from-gray-400 to-emerald-200 bg-clip-text text-transparent;
	}
</style>
