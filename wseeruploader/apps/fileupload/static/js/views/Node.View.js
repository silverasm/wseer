define([
	"jquery",
	"underscore",
	"backbone",
	"text!app/templates/Node.Template.html",
	"text!app/templates/NodeDropped.Template.html",
	"app/views/NodeModal.View"
], function(
	$,
	_,
	Backbone,
	NodeTemplate,
	NodeDroppedTemplate,
	NodeModalView
) {
	var NodeView = Backbone.View.extend({
		className: "node",
		initialize: function() {
			this.app = this.options.app;
			this.parent = this.options.parent; // parent NodeModal
			this.model = this.options.model;
			this.droppable = true;

			var that = this;
			this.model.on("change", _.bind(this.renderDropped, this));
			this.model.children.on("reset", _.bind(this.renderChildren, this));
			this.model.children.on("add", function(model) {
				that.renderChild(model);
			});

		},
		render: function() {
			this.$el.html(_.template(NodeTemplate));
			if (this.model.get("tag")) {
				this.renderDropped();
				this.createModal();
				this.showDropped();
			}
			this.renderChildren();

			return this;
		},
		renderDropped: function() {
			console.log(this.model);
			this.$(".dropped:first").html(_.template(NodeDroppedTemplate, this.model.attributes));
		},
		removeChildren: function() {
			this.$(".childNodes:first").empty();
		},
		renderChildren: function() {
			this.removeChildren();
			var that = this;
			this.model.children.each(function(model) {
				that.renderChild(model);
			});
		},
		renderChild: function(model) {
			var view = new NodeView({app: this.app, model: model, parent: this.model});
			this.$(".childNodes:first").append(view.render().el);
			this.app.views[model.cid] = view;
		},
		events: {
			// drag events
			"dragover .undropped:first": "dragover",
			"dragenter .undropped:first": "dragenter",
			"dragleave .undropped:first": "dragleave",
			"drop .undropped:first": "drop",
			// "hidden .modal:first": "showDropped",
			"click .edit:first": "edit",
			"click .addChild:first": "addChild",
			"click .remove:first": "removeNode"
		},
		dragover: function(e) {
			e.preventDefault();
		},
		dragenter: function(e) {
			this.$(".undropped:first").addClass("dragenter");
		},
		dragleave: function() {
			this.$(".undropped:first").removeClass("dragenter");
		},
		drop: function(e) {
			if (this.droppable) {
				this.tag = this.app.dragTarget.view; // tagView
				// this.app.dragTarget = undefined;

				var name = this.app.dragTarget.name;
				if (this.app.dragTarget.type === "tag") {
					this.model.set("tag", name);
					this.tag.disableTag();
				} else {
					this.model.set("attr", name)
					this.tag.disableAttr(name);
				}
				this.createModal();
				this.modal.open();
				this.showDropped();

				this.dragleave();
				this.droppable = false;
			}

		},
		createModal: function() {
			this.modal = new NodeModalView({
				app: this.app, 
				model: this.model, 
				parent: this.parent
			});
			$("#modal").append(this.modal.render().el);
		},
		showDropped: function() {
			this.$(".undropped:first").hide();
			this.$(".dropped:first").show();

		},
		edit: function() {
			this.modal.open();
		},
		addChild: function() {
			this.model.children.add({app: this.app});
		},
		/*
		remove the node:
			1.  from the DOM, remove all children and itself if it is not root.
			2.  from the model, remove itself from its parent collection if it is not root.
				if it is root, send a message to create a new model and view
		*/
		removeNode: function() {
			this.$el.remove();
			if (this.parent) {
				this.parent.children.remove(this.model);
				
			} else {
				this.app.mediator.publish("node:removed", {});
			}
		}
	});

	return NodeView;
});