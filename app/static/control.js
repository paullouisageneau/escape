
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#console',			// the vue instance controls the element whose id is "control"
	data: {
		enabled: [],		// will contain the indexes of enabled toggles
		startTime: 0,		// timestamp at which the chrono was started
		chrono: '00:00:00',			// the chrono as displayed (HH:MM:SS)
		inputClue: '',		// the clue input from the user
		clues: [],			// all the sent clues
		show: false		// last clue is visible
	},
	mounted: function() {
		// Initialize chrono
		fetch('/api/chrono').then((response) => {
			return response.json();
		}).then((chrono) => {
			if(chrono.start) {
				this.startTime = chrono.start;
			}
		});
		
		// Initialize clues
		fetch('/api/clues').then((response) => {
			return response.json();
		}).then((array) => {
			this.clues = array.map(c => c.text);
		});
		
		// Check if last clue is visible
		fetch('/api/clues/hide').then((response) => {
			return response.json();
		}).then((clueMsg) => {
			this.show = !clueMsg.hide;
		});

		// Initialize toggles
		fetch('/api/toggles').then((response) => {
			return response.json();
		}).then((array) => {
			// Initialize enabled with the indexes of the enabled toggles
			this.enabled = array.map((t, i) => t.value ? i.toString() : null).filter(i => i)
			
			// Now watch enabled for changes and post them
			this.$watch('enabled', function(array, oldArray) {
				function doPost(i, value) {
					const data = {
						value,
					}
					fetch(`/api/toggles/${i}`, {
						method: 'POST',
						body: JSON.stringify(data),
						headers: {
							'Content-Type': 'application/json'
						}
					});
				};
				array.filter(i => !oldArray.includes(i)).forEach(i => doPost(i, true));
				oldArray.filter(i => !array.includes(i)).forEach(i => doPost(i, false));
			});
		});
		
		// Setup update callback every second
		setInterval(this.update, 1000);
	},
	methods: {
		start: function() {
			this.startTime = time();
		},
		trigger: function(i) {
			fetch(`/api/triggers/${i}`, {
				method: 'POST',
			});
		},
		update: function() {
			// The chrono must be updated each second
			if(this.startTime > 0) {
				const t = Math.max(time() - this.startTime, 0);
				const h = Math.floor(t/3600);
				const m = Math.floor(t/60)%60;
				const s = Math.floor(t%60);
				this.chrono = `${("0"+h).slice(-2)}:${("0"+m).slice(-2)}:${("0"+s).slice(-2)}`;
			}
		},
		sendClue: function() {
			if(!this.inputClue) {
				alert("Entrez d'abord un indice.");
				return;
			}
			const data = {
				text: this.inputClue
			};
			fetch('/api/clues', {
				method: 'POST',
				body: JSON.stringify(data),
				headers: {
					'Content-Type': 'application/json'
				}
			}).then((response) => {
				return response.json();
			}).then((clue) => {
				this.clues.push(clue.text); this.show = !clue.hide;
			});
			this.inputClue = '';
		},
		hideClue: function() {
			fetch('/api/clues/hide', {
				method: 'POST',
			}).then((response) => {
			return response.json();
			}).then((clueMsg) => {
			this.show = !clueMsg.hide;
			});
		},
		reset: function() {
			if(confirm("Voulez-vous vraiment réinitialiser la salle ?")) {
				fetch('/api/reset', {
					method: 'POST',
				}).then(() => {
					location.reload();
				});
			}
		},
	},
	watch: {
		startTime: function(value, oldValue) {
			if (value > time()) {
				this.startTime = time();
				return;
			}
			const data = {
				start: this.startTime,
			};
			fetch('/api/chrono', {
				method: 'POST',
				body: JSON.stringify(data),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			this.update();
		}
	}
});
