export type MediaQueryName = keyof typeof mediaQueryMap;
import { writable, derived } from 'svelte/store';

export const mediaQueryMap = {
	sm: '(min-width: 640px)',
	md: '(min-width: 768px)',
	lg: '(min-width: 1024px)',
	xl: '(min-width: 1280px)',
	'2xl': '(min-width: 1536px)'
};

const noop = (cb: (e: MediaQueryListEvent) => void) => () => cb;

export default function mediaBreakPoints(bp: MediaQueryName) {
	if (typeof window === 'undefined') {
		return { matches: false, subscribe: noop };
	}

	const matchMedia = window.matchMedia(mediaQueryMap[bp]);
	return {
		matches: matchMedia.matches,
		subscribe: (cb: (e: MediaQueryListEvent) => void) => {
			matchMedia.addEventListener('change', cb);
			return () => matchMedia.removeEventListener('change', cb);
		}
	};
}

export const mediaBreakPoints$ = (bp: MediaQueryName) => {
	const mbp = mediaBreakPoints(bp);
	const matches$ = writable(mbp.matches);
	mbp.subscribe((e) => matches$.set(e.matches));

	return derived(matches$, (v) => v);
};
