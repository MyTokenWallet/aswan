$(function () {
    // Action Menus -- Navigation Menu's Correspondence
    var actionPages = {
        '/permissions/user/update/': "/permissions/users/",
        '/permissions/group/create/': "/permissions/groups/",
        '/permissions/group/update/': "/permissions/groups/",
        '/permissions/uri_group/create/': "/permissions/uri_groups/",
        '/permissions/uri_group/update/': "/permissions/uri_groups/",

        '/rules/menu/create/': "/rules/menu/list/",

        '/strategy/bool_strategy/test/': "/strategy/bool_strategy/list/",
        '/strategy/bool_strategy/create/': "/strategy/bool_strategy/list/",

        '/strategy/freq_strategy/create/': "/strategy/freq_strategy/list/",
        '/strategy/freq_strategy/test/': "/strategy/freq_strategy/list/",

        '/strategy/user_strategy/create/': "/strategy/user_strategy/list/",
        '/strategy/user_strategy/test/': "/strategy/user_strategy/list/",

        '/strategy/menu_strategy/create/': "/strategy/menu_strategy/list/",
        '/strategy/menu_strategy/test/': "/strategy/menu_strategy/list/",

        '/rule/create/': "/rule/list/",
        '/rule/detail/': "/rule/list/",
        '/rule/edit/': "/rule/list/",
        '/rule/test/': "/rule/list/",
    };
    // Define the current navigation menu
    var currentPath = actionPages[window.location.pathname] ? actionPages[window.location.pathname] : window.location.pathname;
    // Select the current navigation a label
    var selector = 'a[href="' + currentPath + '"]';
    var currentNav = $(selector);
    // Control Parent Menu Highlight
    currentNav.parents('li.siderbar').addClass('active');
    // Control parent menu expansion
    currentNav.parents('ul.nav').addClass('collapse in');

    // Controls the appearance of a one-two-level menu without a submenu
    $("ul:not(:has(li))").parent().addClass('hide');
});