declare namespace NodeJS {
	export interface ProcessEnv {
		NODE_ENV: 'development' | 'production';
		FIREBASE_CONFIG: object & { apiKey: string };
	}
}
