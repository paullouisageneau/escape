
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#display',			// the vue instance controls the element whose id is "display"
	data: {
		video: null,
		audio: null,
	},
	mounted: function() {
		const events = new EventSource('/events');
		events.addEventListener('video', (event) => {
			this.video = event.data;
		});
		events.addEventListener('audio', (event) => {
			this.audio = event.data;
		});
	}
});

