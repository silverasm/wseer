require.config({
    baseUrl: STATIC_URL + "js/contrib/",
    paths: {
        "app": "..",
        "underscore": "underscore",
        "backbone": "backbone",
        "bootstrap": "bootstrap",
        "d3": "d3.v3",
        "mediator": "mediator"
    },
    shim: {
        "underscore": {
            exports: "_"
        },
        "backbone": {
            deps: ["underscore", "jquery"],
            exports: "Backbone"
        },
        "d3": {
            exports: "d3"
        }
    }
});

require([
    "jquery",
    "underscore",
    "backbone",
    "mediator",
    "app/views/App.View"
], function(
    $,
    _,
    Backbone,
    Mediator,
    AppView
) {

    // bugs: disable already dropped tags
    var input,
        app = {};
    app.contentHash = {};
    app.contentNested = {};
    app.badges = {document: "badge-warning", subunit: "badge-success", metadata: "badge-important"};
    app.nameBadges = {sentence: "badge-info", title: "badge-inverse"};
    app.btnTypes = {tag: "btn-primary", attr: "btn-info"};
    app.views = {};
    app.mediator = new Mediator();

    $.get(XML_FILE, function(data) {

        var recurseEl = function(el) {
            var children = $(el).children(),
                attributes = el.attributes,
                obj = {};

            obj.tagName = $(el).prop('tagName');

            obj.attributes = {};
            _.each(attributes, function(attr) {
                obj.attributes[attr.nodeName] = attr.nodeValue;
            });
            

            obj.children = [];
            if (children.length > 0) {
                _.each(children, function(child) {
                    obj.children.push(recurseEl(child));
                });
            } else {
                // assumes text is only on leaf nodes
                obj.text = $(el).text();
            }

            return obj;

        }

        input = recurseEl($(data).children()[0]);

        var appView = new AppView({input: input, app: app});
        appView.render();
    });

    window.app = app;
});