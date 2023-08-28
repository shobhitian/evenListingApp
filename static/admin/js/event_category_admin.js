


function changeStatus(categoryId) {
    const url = `/admin/events/eventcategory/${categoryId}/change_status/`;
  
    // Get the CSRF token from the cookie
    const csrftoken = getCookie('csrftoken');
  
    // Make the API request with the CSRF token
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({}),
    })
      .then((response) => {
        if (response.ok) {
          location.reload();  // Refresh the page after successful status change
        } else {
          throw new Error('Failed to update status.');
        }
      })
      .catch((error) => {
        alert(error.message);
      });
  }
  
  // Function to get the value of a cookie by its name
  function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }
  