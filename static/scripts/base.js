function onGapiLoadCallback() {
  runAfterLoadingGapi();
}

function onSignIn(googleUser) {
  const token = googleUser.getAuthResponse().id_token;
  $.ajax({
    type: 'POST',
    url: '/login-with-google', // TODO: Implement CSRF
    data: JSON.stringify({
      token: token
    }),
    contentType: 'application/json; charset=utf-8',
  }).done(function(result) {
    window.location.reload(true);
  }).fail(function(jqXHR) {
    window.alert(jqXHR.responseText);
  });
}

function runAfterLoadingGapi(callback) {
  gapi.load('auth2', function() {
    gapi.auth2.init().then(function() {
      if (callback) {
        callback();
      }
    });
  });
}

function onSignOut() {
  // Ensure gapi.auth2 is loaded
  if (!gapi || !gapi.auth2) {
    runAfterLoadingGapi(onSignOut);
    return;
  }

  const auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    window.location = '/logout';
  });
}