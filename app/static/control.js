
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#console',			// the vue instance controls the element whose id is "control"
	data: {
		cameras: [],	// will contain the camera URLs
		toggles: [],	// will contain the toggles
		enabled: [],	// will contain the indexes of the enabled toggles
	},
	mounted: function() {
		// Initialize data
		fetch('/api/cameras').then((response) => {
			return response.json();
		}).then((array) => {
			this.cameras = array;
		});
		fetch('/api/toggles').then((response) => {
			return response.json();
		}).then((array) => {
			this.toggles = array;
			
			// Initialize enabled with the indexes of the enabled toggles
			this.enabled = array.map((t, i) => t.value ? i.toString() : null).filter(i => i)
			
			// Now watch enabled for changes and post them
			this.$watch('enabled', function(array, oldArray) {
				function doPost(i, value) {
					data = {
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
	}
});
