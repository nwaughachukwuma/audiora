import { initializeApp } from 'firebase/app';
import { initializeFirestore } from 'firebase/firestore';
import { refs } from './firebase.firestore';
import { browser } from '$app/environment';
import { env } from '@env';
import { initAnalytics } from './firebase.analytics';

export const app = initializeApp(env.FIREBASE_CONFIG);
export const firestore = initializeFirestore(app, {
	experimentalAutoDetectLongPolling: browser,
	localCache: browser ? { kind: 'persistent' } : void 0
});

export const dbRefs = refs(firestore);

initAnalytics(app);
