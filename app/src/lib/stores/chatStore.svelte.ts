import { setContext, getContext } from 'svelte';
import { persisted } from 'svelte-persisted-store';

const CONTEXT_KEY = {};
const CHAT_SESSION_KEY = 'CHAT_SESSION_KEY';

export type ChatItem = {
	id: string;
	content: string;
	role: 'user' | 'assistant';
	loading?: boolean;
};

export function setChatSession(sessionId: string) {
	const chatSession$ = persisted<ChatItem[]>(`${CHAT_SESSION_KEY}_${sessionId}`, []);

	return setContext(CONTEXT_KEY, {
		chatSession$
	});
}

export type ChatSession = ReturnType<typeof setChatSession>;
export const getChatSession = (): ChatSession => getContext(CONTEXT_KEY);
