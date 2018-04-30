
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#display',			// the vue instance controls the element whose id is "display"
	data: {
		video: null,
	},
	mounted: function() {
		const events = new EventSource('/display/events');
		events.onmessage = (message) => {
			const event = JSON.parse(message.data);
			switch(event.action) {
				case 'play':
					this.video = event.target;
					break;
			}
		};
	}
});

