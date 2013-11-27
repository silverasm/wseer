define([
	"jquery",
	"underscore",
	"backbone",
	"app/models/Node.Model",
	"app/views/Node.View",
	"app/views/Content.View",
	"app/views/Tag.View"
], function(
	$,
	_,
	Backbone,
	NodeModel,
	NodeView,
	ContentView,
	TagView
) {
	return Backbone.View.extend({
		el: "body",
		initialize: function() {
			// inp = input
			this.input = this.options.input;
			this.app = this.options.app;

			this.app.mediator.subscribe("node:removed", _.bind(this.renderNodes, this));
		},
		render: function() {
			var that = this;
			this.renderNodes(this.fetchFromLocal());
			// when done rendering content, render tag
			this.renderContent(function() {
				that.renderTag();
			});
		},
		renderNodes: function(nodes) {
			nodes.type = "document";
			nodes.app = this.app;
			var model = this.topModel = new NodeModel(nodes),
				view = new NodeView({app: this.app, model: model});
			this.$("#tagHierarchy").append(view.render().el);
			this.app.views[model.cid] = view;
		},
		renderTag: function() {
			var view = new TagView({obj: this.app.contentNested, app: this.app});
			this.$("#tagContainer").append(view.render().el);

		},
		renderContent: function(callback) {
			var view = new ContentView({obj: this.input, app: this.app});
			this.$("#content").append(view.render().el);

			callback();
		},
		events: {
			"click .save": "saveToLocal"
		},
		/*
		save to local storage, do not hit the server unless the user is done
		*/
		saveToLocal: function() {
			localStorage["nodes"] = JSON.stringify(this.topModel);
		},
		fetchFromLocal: function() {
			var nodes = (localStorage["nodes"] ? $.parseJSON(localStorage["nodes"]) : {})
			return nodes;
		}
	});
});