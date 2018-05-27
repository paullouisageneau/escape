
const ve = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#evac',			// the vue instance controls the element whose id is "evac"
	data: {
		startTime: 0,	// timestamp at which the chrono was started
		stopTime: 0,	// timestamp at which the chrono was stopped
		elapsed: 0,		// seconds elapsed since startTime
		chrono: '00:00:00',	// the chrono as displayed (HH:MM:SS)
		gameState: [],		// State of the game : actions selected by the players
		actions: [],
		nbActions: 2,	
		casualties: 10,		// number of casualties
		victory: false,
		debug: ''
	},
	mounted: function() {
		// Initialize game state
		getJson('/evacuation/action', (data) => {
			this.gameState = data.gameState;
			this.actions = data.actions;
			this.casualties = data.casualties;
			this.victory = data.victory;
		});
	},
	methods: {
		sendAction: function(item) {
			// Send new action
			postJson('/evacuation/action', {
				order: 'execute', action: item
			}, (data) => {
			this.gameState = data.gameState;
			this.casualties = data.casualties;
			this.victory = data.victory;
			});
		},
		abortAction: function(item) {
			// Send new action
			postJson('/evacuation/action', {
				order: 'abort', action: item
			}, (data) => {
			this.gameState = data.gameState;
			this.casualties = data.casualties;
			this.victory = data.victory;
			});
		}
	}
});
