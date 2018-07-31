
let chronoOffset = 0;
let chronoReversed = false;

const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#camera',			// the vue instance controls the element whose id is "camera"
	data: {
		mainCamera: null,
		enabledMics: [],
	},
	mounted: function() {
		this.mainCamera = '0';
	},
	methods: {
		attachMainCamera: function(cameraId) {
			const element = document.getElementById(`camera-${cameraId}`);
			const main = document.getElementById('main-camera');
			main.appendChild(element);
			this.playVideo(element.querySelector('video'), false);
		},
		detachMainCamera: function(cameraId) {
			const element = document.getElementById(`camera-${cameraId}`);
			const placeholder = document.getElementById(`placeholder-${cameraId}`);
			placeholder.appendChild(element);
			this.playVideo(element.querySelector('video'), true);
		},
		playVideo: function(video, muted) {
			if(!video) return;
			video.muted = muted;
			const playPromise = video.play();
			if(playPromise !== undefined) {
				playPromise.catch(e => {});
			}
		}
	},
	watch: {
		mainCamera: function(value, oldValue) {
			if(oldValue) {
				this.detachMainCamera(oldValue);
			}
			if(value) {
				this.attachMainCamera(value);
			}
		}
	}
});

