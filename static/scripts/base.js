function onGapiLoadCallback() {
  /**
   * Called when Google JS SDK is loaded
   */
  runAfterLoadingGapi();
}

function onSignIn(googleUser) {
  /**
   * Called when user signs in
   */
  const token = googleUser.getAuthResponse().id_token;
  $.ajax({
    type: 'POST',
    url: '/login-with-google',
    data: JSON.stringify({
      token: token
    }),
    contentType: 'application/json; charset=utf-8',
  }).done(function (result) {
    // Reload the page
    window.location.reload(true);
  }).fail(function (jqXHR) {
    // Show an alert to the user of the error message
    window.alert(jqXHR.responseText);
  });
}

function runAfterLoadingGapi(callback) {
  /**
   * Initializes `gapi`'s `auth2` module
   * If `callback` is specified, `callback` will be called
   *  after initialization
   */
  gapi.load('auth2', function () {
    gapi.auth2.init().then(function () {
      if (callback) {
        callback();
      }
    });
  });
}

function onSignOut() {
  /**
   * Called when user logouts
   */

  // Ensure gapi.auth2 is loaded
  if (!gapi || !gapi.auth2) {
    runAfterLoadingGapi(onSignOut);
    return;
  }

  const auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    // Go to the `logout` endpoint
    window.location = '/logout';
  });
}