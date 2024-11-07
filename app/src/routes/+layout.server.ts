import type { LayoutServerLoad } from './$types';

export const ssr = true;
export const prerender = false;
export const load: LayoutServerLoad = ({ locals }) => {
	return {
		sessionId: locals.sessionId
	};
};
