define([
	"jquery",
	"underscore",
	"backbone",
	"app/models/Node.Model"
], function(
	$,
	_,
	Backbone,
	NodeModel
) {
	
	// var NodeModel = require('app/models/Node.Model');
	return Backbone.Collection.extend({
		initialize: function() {
			NodeModel = NodeModel || require("app/models/Node.Model");
			this.model = NodeModel;

		}
	});
});