define([
	"jquery",
	"underscore",
	"backbone",
	"text!app/templates/Content.Template.html"
], function(
	$,
	_,
	Backbone,
	ContentTemplate
) {
	var ContentView = Backbone.View.extend({
		className: "contentLine",
		initialize: function() {
			this.parent = this.options.parent; // parent Backbone.View
			this.app = this.options.app;
			this.obj = this.options.obj;

			this.id = (this.parent ? this.parent.id + this.obj.tagName : this.obj.tagName);

			var exists = this.app.contentHash[this.id];
			if (this.parent && !exists) {
				var nest = {};
				this.nested = nest[this.id] = [];
				this.parent.nested.push(nest);
			} else if (this.parent) {
				this.nested = exists[0].nested;
			} else {
				this.nested = this.app.contentNested[this.id] = [];
			}

			if (exists) {
				this.app.contentHash[this.id].push(this);
			} else {
				this.app.contentHash[this.id] = [this];
			}
		},
		render: function() {

			this.$el.html(_.template(ContentTemplate, this.obj));

			var that = this;
			_.each(this.obj.children, function(child) {
				var childView = new ContentView({obj: child, parent: that, app: that.app});
				that.$(".childrenContainer:first").append(childView.render().el);
			});

			return this;
		},
		highlight: function() {
			this.$el.addClass("highlight");
			var top = this.$el.offset().top - 25;
			$(window).scrollTop(top);
		}
	});

	return ContentView;
});