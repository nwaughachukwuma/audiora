import { browser } from '$app/environment';
import { getCustomSources$ } from '@/db/db.customSources';
import { getSession$ } from '@/db/db.session';
import type { ContentCategory } from '@/utils/types';
import { setContext, getContext } from 'svelte';
import { persisted } from 'svelte-persisted-store';
import { derived, writable } from 'svelte/store';

const CONTEXT_KEY = {};
export const SESSION_KEY = 'AUDIOCAST_SESSION';

export type ChatItem = {
	id: string;
	content: string;
	role: 'user' | 'assistant';
	loading?: boolean;
};

export type Session = {
	id: string;
	category: ContentCategory;
	chats: ChatItem[];
	title: string;
	nonce: number;
	completed?: boolean;
	summary?: string;
};

export function getSessionItems() {
	return Object.entries(localStorage)
		.filter(([key]) => key.startsWith(SESSION_KEY))
		.map(
			([key, value]) => [key.replace(`${SESSION_KEY}_`, ''), JSON.parse(value) as Session] as const
		)
		.filter(([_, v]) => Boolean(v));
}

export function setSessionContext(sessionId: string) {
	const session$ = persisted<Session | null>(`${SESSION_KEY}_${sessionId}`, null);
	const sessionId$ = writable(sessionId);
	const sessionCompleted$ = derived(session$, ($session) => !!$session?.completed);

	const fetchingSource$ = writable(false);
	const audioSource$ = persisted<string>(`AUDIOCAST_SOURCE_${sessionId}`, '');

	const sessionItems$ = derived(session$, (v) => (browser || v ? getSessionItems() : []));

	return setContext(CONTEXT_KEY, {
		session$,
		sessionId$,
		sessionCompleted$,
		fetchingSource$,
		audioSource$,
		customSources$: getCustomSources$(sessionId),
		sessionModel$: getSession$(sessionId),
		sessionItems$,
		startSession: (category: ContentCategory) => {
			session$.set({
				id: sessionId,
				category,
				title: 'Untitled',
				nonce: Date.now(),
				chats: []
			});
			return session$;
		},
		addChatItem(chatItem: ChatItem) {
			session$.update((session) => {
				if (session) session.chats.push(chatItem);
				return session;
			});
			return chatItem;
		},
		updateChatItem(update: { id: string } & Partial<ChatItem>) {
			session$.update((session) => {
				if (!session) return session;

				const chats = session.chats.map((item) =>
					item.id === update.id ? { ...item, ...update } : item
				);
				session.chats = chats;
				return session;
			});
		},
		updateChatContent: (chatId: string, chunk: string) => {
			session$.update((session) => {
				if (!session) return session;

				const chats = session.chats.map((i) =>
					i.id === chatId ? { ...i, loading: false, content: i.content + chunk } : i
				);
				session.chats = chats;
				return session;
			});
		}
	});
}

export type SessionContext = ReturnType<typeof setSessionContext>;
export const getSessionContext = (): SessionContext => getContext(CONTEXT_KEY);
