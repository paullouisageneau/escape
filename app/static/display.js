
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#display',			// the vue instance controls the element whose id is "display"
	data: {
		video: null,
		audio: null
	},
	mounted: function() {
		const events = new EventSource('/api/events');
		events.addEventListener('video', (event) => {
			this.video = event.data;
		});
		events.addEventListener('audio', (event) => {
			this.audio = event.data;
		});
	}
});



const chr = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#chrono',			// the vue instance controls the element whose id is "chrono"
	data: {
		startTime: 0,
		chrono: '05:00:00'
	},
	mounted: function() {
		// Initialize chrono
		fetch('/api/chrono').then((response) => {
			return response.json();
		}).then((chrono) => {
			if(chrono.start) {
				this.startTime = chrono.start;
				const t = Math.max(time() - this.startTime, 0);
				const h = 5+Math.floor(t/3600);
				const m = Math.floor(t/60)%60;
				const s = Math.floor(t%60);
				this.chrono = `${("0"+h).slice(-2)}:${("0"+m).slice(-2)}:${("0"+s).slice(-2)}`;
			}
		});
		// Check if chrono is started every second
		setInterval(this.checkChrono, 1000);
		// Setup update callback every second
		setInterval(this.update, 1000);
		},
	methods: {
		checkChrono: function(){
			fetch('/api/chrono').then(
				(response) => {return response.json();}
				).then(
				(chrono) => {if(chrono.start) { this.startTime = chrono.start; } else {this.startTime=0;}}
				);
		},
		update: function() {
			// The chrono must be updated each second
			if(this.startTime > 0) {
				const t = Math.max(time() - this.startTime, 0);
				const h = 5+Math.floor(t/3600);
				const m = Math.floor(t/60)%60;
				const s = Math.floor(t%60);
				this.chrono = `${("0"+h).slice(-2)}:${("0"+m).slice(-2)}:${("0"+s).slice(-2)}`;
			} else { this.chrono = '05:00:00';}
		}
	}
});


const idc = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#clues',			// the vue instance controls the element whose id is "chrono"
	data: {
		clue: '',
		show: false
	},
	mounted: function() {
		// Check if a clue is to be displayed every second
		setInterval(this.checkClue, 1000);
		},
	methods: {
		checkClue: function(){
			fetch('/api/clues/hide').then(
				(response) => {return response.json();}
				).then(
				(clueMsg) => {if(clueMsg.hide) {
					this.show = false; this.clue='';
					} else {this.show = true; this.clue = clueMsg.text;}}
				);
			}
		}
});
