;(function (define) {
    'use strict';

    define(['jquery',
            'underscore',
            'backbone',
            'js/dashboard/views/course_list_tabbed_view'
        ], function ($, _, Backbone, CourseListTabbedView) {
            return function () {
                var courseListTabbedView = new CourseListTabbedView();
                courseListTabbedView.render();
            };
        });

}).call(this, define || RequireJS.define);
