export function getShareableLink(sessionId: string) {
	return `${location.origin}/audiocast/${sessionId}`;
}

export function getShareTitle(sessionTitle: string) {
	return `Listen to this AI-generated audio 🎧 about ${sessionTitle} 🔥`.replace(/\n+/, '') + '\n';
}
