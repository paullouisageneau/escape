
// Returns Unix time (i.e. seconds since Epoch)
function time() {
	return Math.floor(Date.now()/1000);
}

// Format seconds as string "HH:MM:SS"
function formatTime(secs) {
	const h = Math.floor(secs/3600);
	const m = Math.floor(secs/60)%60;
	const s = Math.floor(secs%60);
	return `${("0"+h).slice(-2)}:${("0"+m).slice(-2)}:${("0"+s).slice(-2)}`;
}
