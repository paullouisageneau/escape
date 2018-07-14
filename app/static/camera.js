
let chronoOffset = 0;
let chronoReversed = false;

const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#camera',			// the vue instance controls the element whose id is "display"
	data: {
		mainCamera: undefined,
	},
	mounted: function() {
		this.mainCamera = 1; // TODO
	},
	methods: {
		attachMainCamera: function(cameraId) {
			const element = document.getElementById(`camera-${cameraId}`);
			const main = document.getElementById(`main-camera`);
			main.appendChild(element);
		},
		detachMainCamera: function(cameraId) {
			const element = document.getElementById(`camera-${cameraId}`);
			const placeholder = document.getElementById(`placeholder-${cameraId}`);
			placeholder.appendChild(element);
		},
	},
	watch: {
		mainCamera: function(value, oldValue) {
			if(oldValue) {
				this.detachMainCamera(oldValue);
			}
			if(value) {
				this.attachMainCamera(value);
			}
		},
	}
});

