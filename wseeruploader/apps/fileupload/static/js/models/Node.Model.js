define([
	"jquery",
	"underscore",
	"backbone",
	"app/collections/Nodes.Collection"
], function(
	$,
	_,
	Backbone,
	NodesCollection
) {
	var NodeModel = Backbone.Model.extend({
		initialize: function() {
			this.app = this.attributes.app;
			this.attributes.type ? this.setType(this, this.attributes.type) : this.setType(this, "");
			this.attributes.name ? this.setName(this, this.attributes.name) : this.setName(this, "");
			this.attributes.children ? this.setChildren(this, this.attributes.children) : this.setChildren(this, []);
			if (this.attributes.tag) this.setTag(this, this.attributes.tag);
			if (this.attributes.attr) this.setAttr(this, this.attributes.attr);
			// this.attributes.name = this.attributes.name || "";
			// this.attributes.type = this.attributes.type || "";

			this.on("change:children", this.setChildren);
			this.on("change:type", this.setType);
			this.on("change:name", this.setName);
			this.on("change:tag", this.setTag);
			this.on("change:attr", this.setAttr);
		},
		setChildren: function(model, val) {
			if (!this.children) {
				NodesCollection = NodesCollection || require("app/collections/Nodes.Collection");
				this.children = new NodesCollection();
			}

			// also make sure all children are passed this.app
			var that = this;
			_.each(val, function(obj) {
				obj.app = that.app;
			});
			this.children.reset(val);
		},
		setType: function(model, val) {
			var badge;
			if (val === "document") {
				badge = this.app.badges.document;
			} else if (val === "subunit") {
				badge = this.app.badges.subunit;
			} else if (val === "metadata") {
				badge = this.app.badges.metadata;
			} else {
				badge = "";
			}
			model.set("type", val, {silent: true});
			model.set("badge_type", badge);
		},
		/*
		when a name is set or changed, we must first check:
			1.  was it set to "sentence" or "title"?  if so, make sure it is unique.
			2.  set the name_badge to the appropriate badge.
		*/
		setName: function(model, val) {
			var badge = "",
				views = _.chain(this.app.views)
					.values()
					.filter(function(view) {
						return view.model.get("name") === val;
					}).value();
			if (val === "title") {
				badge = this.app.nameBadges.title;
			} else if (val === "sentence") {
				badge = this.app.nameBadges.sentence;
			}
			model.set("name_badge", badge);

			// if the value is not unique
			if (views.length > 1) {
				_.each(views, function(view) {
					if (view.model !== model) {
						view.model.set("name", "");
						// todo: send a warning message
					}
				});
			}
		},
		setTag: function(model, val) {
			if (val) {
				model.set("attr", "");
				model.set("btn_type", this.app.btnTypes.tag);
			}
		},
		setAttr: function(model, val) {
			if (val) {
				model.set("tag", "");
				model.set("btn_type", this.app.btnTypes.attr);
			}
		},
		toJSON: function() {
			var relevant_keys = ["tag", "type", "name"],
				json = {};

			_.each(this.attributes, function(val, key) {
				if (_.contains(relevant_keys, key)) {
					json[key] = val;
				}
			});

			// take care of the children
			json.children = this.children.toJSON();

			return json;
		}
	});

	// exports.NodeModel = NodeModel;
	return NodeModel;
});