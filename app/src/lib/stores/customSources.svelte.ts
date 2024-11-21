import { setContext, getContext } from 'svelte';
import { writable } from 'svelte/store';

export type LinkSources = {
	type: 'link';
	url: string;
};

export type CopyPasteSources = {
	type: 'copy/paste';
};

export type Sources = (LinkSources | CopyPasteSources) & {
	id: string;
	content_type: 'text/plain' | 'text/html' | 'application/pdf';
	content: string;
	created_at: string;
};

const CONTEXT_KEY = {};

export const setCustomSources = (_sessionId: string) => {
	const sources$ = writable<Sources[] | null>(null);

	return setContext(CONTEXT_KEY, {
		sources$,
		addSource: (source: Sources) => {
			sources$.update((sources) => (!sources ? sources : [...sources, source]));
			return sources$;
		}
	});
};

export type CustomSourcesType = ReturnType<typeof setCustomSources>;
export const getCustomSources = () => getContext<CustomSourcesType>(CONTEXT_KEY);
