
let chronoOffset = 0;
let chronoReversed = false;

const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#camera',			// the vue instance controls the element whose id is "camera"
	data: {
		selectedCam: null,
		enabledMics: [],
	},
	mounted: function() {
		this.selectedCam = 0;
	},
	methods: {
		muteCameras: function() {
			const elements = document.querySelectorAll('#cameras video');
			for(e of elements) {
				e.muted = true;
			}
		}
	},
	watch: {
		selectedCam: function(value) {
			this.muteCameras();
			const element = document.querySelector(`#camera-${value} video`);
			if(element) {
				element.muted = false;
			}
		}
	}
});

