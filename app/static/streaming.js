
let janus = null;
let streaming = null;

function initStreaming(id, onSuccess, onError) {
	const videoElement = document.getElementById(id);

	// Initialize the library (all console debuggers enabled)
	Janus.init({debug: "all", callback: function() {
		// Make sure the browser supports WebRTC
		if(!Janus.isWebrtcSupported()) {
			if(onError) onError(new Error("The browser does not support WebRTC"));
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
						if(onSuccess) onSuccess();
					},
					error: function(error) {
						Janus.error("Error attaching plugin", error);
						if(onError) onError(error);
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
									Janus.error("WebRTC error", error);
								}
							});
						}
					},
					onremotestream: function(stream) {
						Janus.debug("Got a remote stream");
						Janus.attachMediaStream(videoElement, stream);
					},
					oncleanup: function() {
						Janus.log("Got a cleanup notification");
					}
				});
			},
			error: function(error) {
				Janus.error("Error creating session", error);
				if(onError) onError(error);
			}
		});
	}});
}

function startStream(selectedStream) {
	Janus.log("Selected stream id #" + selectedStream);
	const body = { "request": "watch", id: parseInt(selectedStream) };
	streaming.send({ "message": body });
}

function stopStream() {
	const body = { "request": "stop" };
	streaming.send({ "message": body });
	streaming.hangup();
}

