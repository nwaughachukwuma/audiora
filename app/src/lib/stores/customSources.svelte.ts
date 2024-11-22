import { getCustomSources$ } from '@/db/db.customSources';
import { setContext, getContext } from 'svelte';

export type LinkSources = {
	source_type: 'link';
	url: string;
};

export type CopyPasteSources = {
	source_type: 'copy/paste';
};

export type Sources = (LinkSources | CopyPasteSources) & {
	id: string;
	content_type: 'text/plain' | 'text/html' | 'application/pdf';
	content: string;
	created_at?: string;
};

const CONTEXT_KEY = {};

export const setCustomSources = (sessionId: string) => {
	const sources$ = getCustomSources$(sessionId);
	return setContext(CONTEXT_KEY, {
		sources$
	});
};

export type CustomSourcesType = ReturnType<typeof setCustomSources>;
export const getCustomSources = () => getContext<CustomSourcesType>(CONTEXT_KEY);
