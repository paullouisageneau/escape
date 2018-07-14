
let janus = null;
let streaming = null;

// Init the streaming
// Note: this function cannot use a promise since onError can be triggered after onInit
function initStreaming(elementId, onInit, onError) {
	const mediaElement = document.getElementById(elementId);

	// Initialize the library (all console debuggers enabled)
	Janus.init({ debug: "all", callback: function() {
		// Make sure the browser supports WebRTC
		if(!Janus.isWebrtcSupported()) {
			Janus.error("WebRTC not supported");
			if(onError) onError("Le navigateur ne supporte pas WebRTC.");
			return;
		}
		// Create session
		janus = new Janus({
			server: window.location.protocol + "//" + window.location.host + "/janus",
			success: function() {
				// Attach to streaming plugin
				janus.attach({
					plugin: "janus.plugin.streaming",
					opaqueId: Janus.randomString(12),
					success: function(pluginHandle) {
						streaming = pluginHandle;
						Janus.log("Plugin attached (" + streaming.getPlugin() + ", id=" + streaming.getId() + ")");
						if(onInit) onInit();
					},
					error: function(error) {
						Janus.error("Error attaching plugin");
						if(onError) onError("Impossible d'initialiser le service de streaming.");
					},
					onmessage: function(msg, jsep) {
						Janus.debug("Got a message");
						if(msg.error) {
							Janus.error("Error during session", msg.error);
							stopStream();
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
									if(onError) onError("La négociation des paramètres audio et vidéo a échoué.");
								}
							});
						}
					},
					onremotestream: function(stream) {
						Janus.debug("Got a remote stream");
						Janus.attachMediaStream(mediaElement, stream);
					},
					oncleanup: function() {
						Janus.log("Got a cleanup notification");
					}
				});
			},
			error: function(error) {
				Janus.error("Error creating session");
				if(onError) onError("Impossible de contacter le service de streaming.");
			}
		});
	}});
}

// Start streaming 
function startStream(streamId) {
	Janus.log(`Selected stream ${streamId}`);
	const body = { "request": "watch", id: streamId };
	streaming.send({ "message": body });
}

function stopStream() {
	const body = { "request": "stop" };
	streaming.send({ "message": body });
	streaming.hangup();
}

