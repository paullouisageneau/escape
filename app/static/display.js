
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
	},
	mounted: function() {
		const events = new EventSource('/api/events');
		
		// Initialize chrono
		fetch('/api/chrono').then((response) => {
			return response.json();
		}).then((chrono) => {
			this.startTime = chrono.start;
			this.stopTime = chrono.stop;
		});
		
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
			this.video = event.data;
		});
		
		// Play audio
		events.addEventListener('audio', (event) => {
			this.audio = event.data;
		});
		
		// Reset room
		events.addEventListener('reset', (event) => {
			this.reset();
		});
		
		// Setup update callback every second
		setInterval(this.update, 1000);
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
			
			// TODO: actual format depends on the room
			this.chrono = formatTime(this.elapsed + 5*60*60);
		},
		reset: function() {
			this.startTime = 0;
			this.stopTime = 0;
			this.video = null;
			this.audio = null;
		}
	},
	watch: {
		startTime: function() {
			this.elapsed = 0;	// Allow the chrono to decrease
			this.update();
		},
		stopTime: function() {
			this.update();
		}
	}
});

