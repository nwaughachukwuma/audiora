import type { LayoutServerLoad } from './$types';
import type { ContentCategory } from '@/utils/types';

export const load: LayoutServerLoad = ({ url }) => {
	const category = url.searchParams.get('category') as ContentCategory | null;
	return {
		category
	};
};
