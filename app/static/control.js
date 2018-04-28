 

const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#console',			// the vue instance controls the element whose id is "control"
	data: {
		cameras: [],		// the array that will contain the camera URLs
	},
	created: function() {
		// Initialize data
		fetch('/api/cameras').then((response) => {
			return response.json();
		}).then((array) => {
			this.cameras = array;
		});
	}
});
