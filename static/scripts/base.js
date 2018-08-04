function onSignIn(googleUser) {
  const token = googleUser.getAuthResponse().id_token;

  $.ajax({
    type: 'POST',
    url: '/login-with-google', // TODO: Implement CSRF
    data: JSON.stringify({
      token: token
    }),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    error: function(jqXHR) {
      window.alert(jqXHR.responseText);
    },
    success: function(result) {
      window.alert('You have successfully logged in.');
    }
  });
}
