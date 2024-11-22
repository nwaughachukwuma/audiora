import { initializeApp, getApps } from 'firebase/app';
import { initializeFirestore } from 'firebase/firestore';
import { refs } from './firebase.firestore';
import { initAnalytics } from './firebase.analytics';
import { browser } from '$app/environment';

// Initialize Firebase
export const app = getApps()[0] || initializeApp(process.env.FIREBASE_CONFIG);
export const firestore = initializeFirestore(app, {
	experimentalAutoDetectLongPolling: browser,
	localCache: browser ? { kind: 'persistent' } : void 0
});

initAnalytics(app);
export const analytics = initAnalytics(app);
export const dbRefs = refs(firestore);
