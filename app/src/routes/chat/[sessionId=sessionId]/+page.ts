import type { PageLoad } from './$types';

export const load: PageLoad = async ({ url, parent }) => {
	const { category } = await parent();
	return {
		category
	};
};
