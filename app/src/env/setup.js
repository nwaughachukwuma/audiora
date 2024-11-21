export const env = {
	NODE_ENV: process.env.NODE_ENV,
	PROJECT_ID: process.env.PROJECT_ID,
	VERSION: process.env.VERSION,
	BUILD_TIME: new Date().toString(),
	API_BASE_URL: process.env.API_BASE_URL,
	IMGPROXY_URL: process.env.IMGPROXY_URL,
	FIREBASE_CONFIG: process.env.FIREBASE_CONFIG
};
