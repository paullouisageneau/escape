
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#display',			// the vue instance controls the element whose id is "display"
	data: {
		video: null,
	},
	mounted: function() {
		const events = new EventSource('/events');
		events.addEventListener('play', (event) => {
			this.video = event.data;
		});
	}
});

