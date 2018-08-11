
Vue.component('controller', {
	delimiters:['${', '}'],
	props: ['camera', 'reversed'],
	data: function() {
		return {
			lastAction: ''
		}
	},
	computed: {
		isReversed: function() {
			return this.reversed && this.reversed.toLowerCase() == "true"; // reversed is an HTML parameter
		}
	},
	mounted: function() {
		this.command('init');
		this.command('stop');
	},
	beforeDestroy: function() {
		this.command('stop');
	},
	methods: {
		command: function(action) {
			if(action != this.lastAction) {
				this.lastAction = action;
				const data = {
					action: this.translate(action)
				};
				postJson(`/api/camera/${this.camera}`, data, () => {}, true);
			}
		},
		translate: function(action) {
			if(this.isReversed) {
				switch(action) {
					case 'up': return 'down';
					case 'down': return 'up';
					case 'left': return 'right';
					case 'right': return 'left';
				}
			}
			return action;
		}
	},
	template: `
		<div class="controller">
			<img src="/static/arrow_up.png" alt="UP" class="control-up enabled" v-on:mousedown="command('up')" v-on:mouseup="command('stop')" v-on:mouseleave="command('stop')"></td>
			<img src="/static/arrow_left.png" alt="LEFT" class="control-left enabled" v-on:mousedown="command('left')" v-on:mouseup="command('stop')" v-on:mouseleave="command('stop')">
			<img src="/static/arrow_right.png" alt="RIGHT" class="control-right enabled" v-on:mousedown="command('right')" v-on:mouseup="command('stop')" v-on:mouseleave="command('stop')">
			<img src="/static/arrow_down.png" alt="DOWN" class="control-down enabled" v-on:mousedown="command('down')" v-on:mouseup="command('stop')" v-on:mouseleave="command('stop')">
			<img src="/static/arrow_center.png" class="control-center">
		</div>`
});
