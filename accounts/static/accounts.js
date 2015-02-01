
var initialize = function(navigator, user, token, urls) {

  navigator.id.watch({
    loggedInUser: user,
    onlogin: function(assertion) {
      $.post(
        urls.login,
        { assertion: assertion, csrfmiddlewaretoken: token }
      ).done(function() { window.location.reload(); }
      ).fail(function() { navigator.id.logout(); });
    },
    onlogout: function() {}
  });

  $('#id_login').on('click', function() {
    navigator.id.request();
  });
};

window.Superlists = {
  Accounts: {
    initialize: initialize
  }
};
