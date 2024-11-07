import { error, redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ url, parent }) => {
	const category = url.searchParams.get('category');
	if (!category) error(400, 'Audio category was not found');

	const { sessionId } = await parent();
	if (url.pathname !== `/${sessionId}`) redirect(307, '/');

	return {
		category
	};
};
