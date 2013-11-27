define([
	"jquery",
	"underscore",
	"backbone",
	"bootstrap",
	"text!app/templates/NodeModal.Template.html",
	"text!app/templates/ModalContent.Template.html",
	"text!app/templates/ModalParentContent.Template.html"
], function(
	$,
	_,
	Backbone,
	modal,
	NodeModalTemplate,
	ModalContentTemplate,
	ModalParentContentTemplate
) {
	return Backbone.View.extend({
		className: "modal hide",
		initialize: function() {
			this.app = this.options.app;
			this.model = this.options.model;
			this.parent = this.options.parent; // parent model

			this.model.on("change", _.bind(this.render, this));
			if (this.parent) this.parent.on("change", _.bind(this.render, this));
		},
		render: function() {
			this.$el.html(_.template(NodeModalTemplate));
			this.renderNode();
			this.renderParent();

			return this;
		},
		renderNode: function() {
			this.$(".nodeAttrs").html(_.template(ModalContentTemplate, this.model.attributes));
		},
		renderParent: function() {
			if (this.parent) {
				this.$(".parentAttrs").html(_.template(ModalParentContentTemplate, this.parent.attributes));
			}
		},
		open: function() {
			this.$el.modal("show");
		},
		events: {
			"click .type input": "typeChanged",
			"click .nameRadio input": "nameRadioChecked",
			"change input.nameText": "nameTextChanged"
		},
		typeChanged: function(e) {
			var val = $(e.target).val();
			this.model.set("type", val);
			this.model.set("name", "");
		},
		nameRadioChecked: function(e) {
			var val = $(e.target).val();
			this.model.set("name", val);
		},
		nameTextChanged: function(e) {
			var val = $(e.target).val();
			this.model.set("name", val);
		}
	});
});