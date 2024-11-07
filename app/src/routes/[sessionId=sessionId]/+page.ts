import { error, redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ url, parent }) => {
	const { sessionId, category } = await parent();
	if (!category) error(400, 'Audio category was not found');
	if (url.pathname !== `/${sessionId}`) redirect(307, '/');

	return {
		category
	};
};
