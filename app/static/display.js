
let chronoOffset = 0;
let chronoReversed = false;

const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#display',			// the vue instance controls the element whose id is "display"
	data: {
		startTime: 0,		// timestamp at which the chrono was started
		stopTime: 0,		// timestamp at which the chrono was started
		elapsed: 0,			// seconds elapsed since startTime
		chrono: '',			// the chrono as displayed
		clue: '',			// the currently displayed clue
		video: null,		// the URL of the playing video, if any
		audio: null,		// the URL of the playing audio, if any
		backgroundAudio: null,	// the URL of the playing audio, if any
	},
	computed: {
		paused: function() {
			return this.stopTime > 0;
		},
		backgroundVolume: function() {
			return this.audio || this.clue ? 0.3 : 1.0;
		}
	},
	mounted: function() {
		const noVideo = window.location.hash && window.location.hash.includes('novideo');
		const noAudio = window.location.hash && window.location.hash.includes('noaudio');
		
		// Initialize chrono
		getJson('/api/chrono', (chrono) => {
			this.startTime = chrono.start;
			this.stopTime = chrono.stop;
		});
		
		// Initialize clue
		getJson('/api/clues/current', (clue) => {
			this.clue = clue.text;
		});
		
		const events = new EventSource('/api/events');
		
		// Chrono update
		events.addEventListener('chrono', (event) => {
			const chrono = JSON.parse(event.data);
			this.startTime = chrono.start;
			this.stopTime = chrono.stop;
		});
		
		// Clue update
		events.addEventListener('clue', (event) => {
			const clue = JSON.parse(event.data);
			this.clue = clue.text;
		});
		
		// Play video
		events.addEventListener('video', (event) => {
			this.video = null;
			if(event.data && !noVideo) {
				Vue.nextTick(() => {
					this.video = event.data;
				});
			}
		});
		
		// Play audio
		events.addEventListener('audio', (event) => {
			this.audio = null;
			if(event.data && !noAudio) {
				Vue.nextTick(() => {
					this.audio = event.data;
				});
			}
		});
		
		// Play background audio
		events.addEventListener('background_audio', (event) => {
			if(!noAudio) {
				const element = document.getElementById('background-audio');
				if(!event.data) {
					if(element) element.pause();
				} 
				else if(event.data == this.backgroundAudio) {
					if(element) element.play();
				}
				else {
					let previousSrc, previousTime;
					if(element) {
						const source = element.getElementsByTagName('source')[0];
						previousSrc = source.src;
						previousTime = element.currentTime;
					}
					this.backgroundAudio = null;
					Vue.nextTick(() => {
						this.backgroundAudio = event.data;
						// Loop on previous background audio if it was present
						if(previousSrc) {
							Vue.nextTick(() => {
								const element = document.getElementById('background-audio');
								if(element) {
									element.loop = false;
									element.onended = () => {
										const source = element.getElementsByTagName('source')[0];
										source.src = previousSrc;
										element.loop = true;
										element.load();
										element.play();
										element.oncanplay = () => {
											element.currentTime = previousTime;
											element.oncanplay = () => {};
										};
									};
								}
							});
						}
					});
				}
			}
		});
		
		// Reset room
		events.addEventListener('reset', (event) => {
			this.reset();
		});
		
		// Setup update callback every second
		setInterval(this.update, 1000);
		this.update();
	},
	methods: {
		update: function() {
			// The chrono must be updated each second
			if(this.startTime > 0) {
				// refTime is the reference to compute elapsed time
				const refTime = this.stopTime > 0 ? this.stopTime : time();
				
				// elapsed is the time since refTime, it must be increasing to avoid seeing the chrono moving back 1 sec when stopTime < time()
				this.elapsed = Math.max(refTime - this.startTime, this.elapsed);
			}
			else {
				this.elapsed = 0;
			}
			
			const t = Math.max(chronoOffset + this.elapsed * (chronoReversed ? -1 : 1), 0);
			this.chrono = formatTime(t);
		},

		reset: function() {
			this.startTime = 0;
			this.stopTime = 0;
			this.clue = '';
			this.video = null;
			this.audio = null;
			this.backgroundAudio = null;
		}
	},
	watch: {
		startTime: function() {
			this.elapsed = 0;	// Allow the chrono to decrease
			this.update();
		},
		stopTime: function() {
			this.update();
		},
		paused: function(value) {
			// Disconnected background audio from chrono
			//const element = document.getElementById('background-audio');
			//if(element) {
			//	if(value) element.pause();
			//	else element.play();
			//}
		},
		backgroundVolume: function(value) {
			const element = document.getElementById('background-audio');
			if(element) {
				element.volume = value;
			}
		}
	}
});

