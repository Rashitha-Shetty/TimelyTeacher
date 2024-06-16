function showMessage() {
    try {
      var messageBox = document.getElementById("messageBox");
      messageBox.style.display = "block";
      setTimeout(function () {
        messageBox.style.display = "none";
      }, 5000); // 5000 milliseconds = 5 seconds
      
    } catch (error) {
      
    }
  }
  
  // Call showMessage function to display the message box
  showMessage();


function confirmLogOut() {
  // Prompt the user for confirmation
  var result = confirm("Are you sure you want to Log Out?");

  // If user confirms, proceed with form submission
  if (result) {
    window.location.href = '/logout';

  } else {
    // If user cancels, prevent the form submission
    return false;
  }
}





// Show loading spinner
function showLoadingSpinner() {
  document.getElementById('loading-spinner').classList.remove('hide');
  document.querySelectorAll('button, a').forEach(element => {
      element.classList.add('disabled-on-load');
  });
}

// Hide loading spinner and enable all buttons and anchor tags
function hideLoadingSpinner() {
  document.getElementById('loading-spinner').classList.add('hide');
  document.querySelectorAll('button, a').forEach(element => {
      element.classList.remove('disabled-on-load');
  });
}

document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', function(e) {
          if (form.checkValidity()) { // Check form validity before submission
              showLoadingSpinner();
          } else {
              hideLoadingSpinner(); // Hide spinner if form submission fails due to missing required fields
          }
      });
  });
});
