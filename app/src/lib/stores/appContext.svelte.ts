import { getContext, setContext } from 'svelte';
import { persisted } from 'svelte-persisted-store';

const CONTEXT_KEY = {};

export const setAppContext = () => {
	const openSettingsDrawer$ = persisted('SETTINGS_DRAWER', false);
	return setContext(CONTEXT_KEY, {
		openSettingsDrawer$
	});
};

export type AppContext = ReturnType<typeof setAppContext>;

export const getAppContext = (): AppContext => getContext(CONTEXT_KEY) || setAppContext();
