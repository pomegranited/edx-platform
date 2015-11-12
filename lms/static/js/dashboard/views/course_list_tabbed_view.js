;(function (define) {
    'use strict';

    define(['backbone', 'underscore', 'gettext',
        'js/dashboard/views/course_list_view',
        'js/components/tabbed/views/tabbed_view'
    ], function (Backbone, _, gettext, CourseListView, TabbedView) {

        var CourseListTabbedView = Backbone.View.extend({

            el: '#wrapper-course-tabs',

            courses: {
                active: {
                    title: gettext('Active'),
                    template: '#active-courses-tpl',
                    url: '/active-courses',
                    index: 0
                },
                completed: {
                    title: gettext('Completed'),
                    template: '#completed-courses-tpl',
                    url: '/completed-courses',
                    index: 1
                }
            },

            initialize: function () {

                this.setElement(this.el);

                this.activeCourseListView = new CourseListView({template: this.courses.active.template});
                this.completedCourseListView = new CourseListView({template: this.courses.completed.template});

                // This slightly tedious approach is necessary
                // to use regular expressions within Backbone
                // routes, allowing us to capture which tab
                // name is being routed to.
                var router = new Backbone.Router();
                _.each([
                    ['content', _.bind(function () {
                        // The backbone router unfortunately usurps the
                        // default behavior of in-page-links.  This hack
                        // prevents the screen reader in-page-link from
                        // being picked up by the backbone router.
                    }, this)],
                    [new RegExp('^([a-z]+-courses)\/?$'), _.bind(this.goToTab, this)]
                ], function (route) {
                    router.route.apply(router, route);
                });

                this.mainView = new TabbedView({
                    tabs: [{
                        title: this.courses.active.title,
                        url: this.courses.active.url,
                        view: this.activeCourseListView
                    }, {
                        title: this.courses.completed.title,
                        url: this.courses.completed.url,
                        view: this.completedCourseListView
                    }],
                    router: router
                });

                Backbone.history.start();
            },

            render: function () {
                this.mainView.setElement(this.el).render();
                return this;
            },
            /**
             * Set up the tabbed view and switch tabs.
             */
            goToTab: function (tab) {

                // Note that `render` should be called first so
                // that the tabbed view's element is set
                // correctly.
                var tabId = tab.split('-')[0];
                this.render();
                this.mainView.setActiveTab(this.courses[tabId].index);
            }
        });

        return CourseListTabbedView;
    });

}).call(this, define || RequireJS.define);
