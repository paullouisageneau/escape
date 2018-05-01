
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#display',			// the vue instance controls the element whose id is "display"
	data: {
		startTime: 0,		// timestamp at which the chrono was started
		chrono: '',			// the chrono as displayed
		clue: '',			// the currently displayed clue
		clueTimeout: null,	// timeout for the displayed clue
		video: null,		// the URL of the playing video, if any
		audio: null,		// the URL of the playing audio, if any
	},
	mounted: function() {
		const events = new EventSource('/api/events');
		
		// Chrono update
		events.addEventListener('chrono', (event) => {
			const chrono = JSON.parse(event.data);
			this.startTime = chrono.start;
		});
		
		// Clue update
		events.addEventListener('clue', (event) => {
			const clue = JSON.parse(event.data);
			this.clue = clue.text;
			if(this.clueTimeout) clearTimeout(this.clueTimeout);
			this.clueTimeout = setTimeout(() => {
				// Clear the clue after timeout
				this.clue = '';
				this.clueTimeout = null;
			}, 10000);
		});
		
		// Reset room
		events.addEventListener('reset', (event) => {
			this.reset();
		});
		
		// Play video
		events.addEventListener('video', (event) => {
			this.video = event.data;
		});
		
		// Play audio
		events.addEventListener('audio', (event) => {
			this.audio = event.data;
		});
		
		// Setup update callback every second
		setInterval(this.update, 1000);
	},
	methods: {
		update: function() {
			if(this.startTime > 0) {
				const secs = Math.max(time() - this.startTime, 0);
				// TODO: actual format depends on the room
				this.chrono = formatTime(secs);
			}
			else {
				this.chrono = '';
			}
		},
		reset: function() {
			this.startTime = 0;
			this.video = null;
			this.audio = null;
			this.update();
		}
	},
	watch: {
		startTime: function() {
			this.update();
		}
	}
});

