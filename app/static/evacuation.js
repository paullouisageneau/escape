
const ve = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#evac',			// the vue instance controls the element whose id is "evac"
	data: {
		startTime: 0,	// timestamp at which the chrono was started
		stopTime: 0,	// timestamp at which the chrono was stopped
		elapsed: 0,		// seconds elapsed since startTime
		chrono: '00:00:00',	// the chrono as displayed (HH:MM:SS)
		gameState: {},		// State of the game : actions selected by the players
		casualties: 10,		// number of casualties
		items: ['1','2','3']
	},
	mounted: function() {
		// Initialize game state
		getJson('/api/evacuation', (data) => {
			this.gameState = data.gameState;
			this.$watch('gameState', function(val,oldVal) {postJson('/api/evacuation',val)} );
		});
	}
});
