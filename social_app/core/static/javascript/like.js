
  $(document).ready(function() {
    $('#likeIn').click(function() {
      var postId = $(this).data('post-id');
      $.ajax({
        url: 'like{{post.id}}',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
          if (response.success) {
            $('#like-button-container').html('<p>You liked this page!</p>');
          } else {
            alert(response.message);
          }
        },
        error: function(xhr, status, error) {
          alert('An error occurred while processing your request.');
        }
      });
    });
  });
