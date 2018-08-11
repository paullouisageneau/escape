
Vue.component('controller', {
	delimiters:['${', '}'],
	props: ['camera'],
	data: function() {
		return {
			
		}
	},
	mounted: function() {
		this.command('init');
	},
	beforeDestroy: function() {
		this.command('stop');
	},
	methods: {
		command: function(action) {
			const data = {
				action,
			};
			const silent = action == 'init' || action == 'stop';
			postJson(`/api/camera/${this.camera}`, data, () => {
			
			}, silent);
		}
	},
	template: `
		<div class="controller">
			<img src="/static/arrow_up.png" alt="UP" class="control-up" v-on:mousedown="command('up')" v-on:mouseup="command('stop')" v-on:mouseleave="command('stop')"></td>
			<img src="/static/arrow_left.png" alt="LEFT" class="control-left" v-on:mousedown="command('left')" v-on:mouseup="command('stop')" v-on:mouseleave="command('stop')">
			<img src="/static/arrow_right.png" alt="RIGHT" class="control-right" v-on:mousedown="command('right')" v-on:mouseup="command('stop')" v-on:mouseleave="command('stop')">
			<img src="/static/arrow_down.png" alt="DOWN" class="control-down" v-on:mousedown="command('down')" v-on:mouseup="command('stop')" v-on:mouseleave="command('stop')">
			<img src="/static/arrow_center.png" class="control-center">
		</div>`
});
