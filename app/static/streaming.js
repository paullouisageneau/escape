
const janusContext = {
	url: window.location.protocol + "//" + window.location.host + "/janus",
	janus: null
};

window.addEventListener('load', () => {
	createJanusSession(janusContext.url)
		.then(() => {
			janusContext.janus = janus;
		})
		.catch((error) => {
			alert(`Erreur: ${error.message}`);
		});
});

Vue.component('streaming', {
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	props: ['type', 'streamId'],
	data: function() {
		return {
			context: janusContext,
			streaming: null,
		}
	},
	computed: {
		isAudio: function() {
			return this.type == "audio";
		},
		elementId: function() {
			return `streaming-${this.streamId}`;
		},
		element: function() {
			return document.getElementById(this.elementId);
		}
	},
	watch: {
		context: function(value, oldValue) {
			if(value.janus && !this.streaming) {
				attachJanusStreaming(this.element, parseInt(this.streamId, 10))
					.then((streaming) => {
						this.streaming = streaming;
					})
					.catch((error) => {
						alert(`Erreur: ${error.message}`);
					});
			}
		}
	},
	template: '<audio v-if="isAudio" id="{{ elementId }}"></audio><video v-else id="{{ elementId }}"></video>'
});


function createJanusSession(url) {
	return new Promise((resolve, reject) => {
		// Initialize the library (all console debuggers enabled)
		Janus.init({ debug: "all", callback: function() {
			// Make sure the browser supports WebRTC
			if(!Janus.isWebrtcSupported()) {
				Janus.error("WebRTC not supported");
				reject(new Error("Le navigateur ne supporte pas WebRTC."));
				return;
			}
			// Create session
			const janus = new Janus({
				server: url,
				success: function() {
					resolve(janus);
				},
				error: function(error) {
					Janus.error("Error creating session");
					reject(new Error("Impossible de contacter le service de streaming."));
				}
			});
		}});
	});
}

function attachJanusStreaming(mediaElement, streamId) {
	return new Promise((resolve, reject) => {
		// Attach to streaming plugin
		janus.attach({
			plugin: "janus.plugin.streaming",
			opaqueId: Janus.randomString(12),
			success: function(pluginHandle) {
				streaming = pluginHandle;
				Janus.log("Plugin attached (" + streaming.getPlugin() + ", id=" + streaming.getId() + ")");
				Janus.log(`Requesting stream ${streamId}`);
				const body = { "request": "watch", id: streamId };
				streaming.send({ "message": body });
			},
			error: function(error) {
				Janus.error("Error attaching plugin");
				reject(new Error("Impossible d'initialiser le service de streaming."));
			},
			onmessage: function(msg, jsep) {
				Janus.debug("Got a message");
				if(msg.error) {
					Janus.error("Error during session", msg.error);
					reject(new Error("La session de streaming a été interrompue."));
					return;
				}
				if(jsep) {
					Janus.debug("Handling SDP");
					// Answer
					streaming.createAnswer({
						jsep: jsep,
						media: { audioSend: false, videoSend: false },	// We want recvonly audio/video
						success: function(jsep) {
							Janus.debug("Got SDP");
							const body = { "request": "start" };
							streaming.send({"message": body, "jsep": jsep});
						},
						error: function(error) {
							Janus.error("WebRTC negociation failed");
							reject(new Error("Le format audio/video n'est pas supporté."));
						}
					});
				}
			},
			onremotestream: function(stream) {
				Janus.debug("Got a remote stream");
				Janus.attachMediaStream(mediaElement, stream);
				mediaElement.play();
				resolve(streaming);
			},
			oncleanup: function() {
				Janus.log("Got a cleanup notification");
			}
		});
	});
}
