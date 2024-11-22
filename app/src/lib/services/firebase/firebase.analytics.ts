import type { FirebaseApp } from 'firebase/app';
import { browser } from '$app/environment';
import { getAnalytics } from 'firebase/analytics';

export async function initAnalytics(app: FirebaseApp) {
	if (!browser) return;
	const analytics = getAnalytics(app);
	analytics.app.automaticDataCollectionEnabled = false;
}
