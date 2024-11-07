import type { LayoutServerLoad } from './$types';
export const load: LayoutServerLoad = ({ url }) => {
	return {
		category: url.searchParams.get('category')
	};
};
