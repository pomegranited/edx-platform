;(function (define) {
    'use strict';

    define(['jquery', 'backbone'], function ($, Backbone) {
            var CourseListView = Backbone.View.extend({

                initialize: function (options) {
                    this.template = options.template;
                },

                render: function () {
                    this.$el.html($(this.template).html());
                    return this;
                }
            });

            return CourseListView;
        });

}).call(this, define || RequireJS.define);
