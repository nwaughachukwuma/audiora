const importPromise = () => import('copy-to-clipboard');
export function copy(text: string): Promise<boolean> {
	return new Promise((resolve) => importPromise().then(({ default: copy }) => resolve(copy(text))));
}
