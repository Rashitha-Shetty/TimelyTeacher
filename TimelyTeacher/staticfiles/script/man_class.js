function closeForm() {
    const formPopup = document.getElementById('popup');
    // formPopup.style.animation = 'zoomOut 0.3s forwards'; // Apply zoom-out animation
    // formPopup.style.display = 'none';
    formPopup.classList.add('hide');
    document.querySelector('.popblur').classList.remove('blur');
    
    // setTimeout(() => {

    // }, 300); // Delay hiding the form to allow animation to complete
}

document.getElementById('set_float').addEventListener('click', function() {
  var saveButton = document.getElementById('saveButton');
  var deleteButton = document.querySelector('#popup [name="delete"]');


  const formPopup = document.getElementById('popup');
  formPopup.classList.remove('hide');
  document.querySelector('.popblur').classList.add('blur');


  // visibility of the popup
  // formPopup.style.animation = 'zoomIn 0.3s forwards';
  document.getElementById('saveButton').classList.remove('hide');
  
  deleteButton.classList.add('hide');
  document.getElementById('editCancelButton')

  var inputs = document.querySelectorAll('#popup input, #popup textarea');
  
  inputs.forEach(function(input) {
    input.disabled = false;
  });

 

  document.getElementById('name').value = "";
      document.getElementById('userName').value = "";
      document.getElementById('password').value = "";
      document.getElementById('confirmPassword').value = "";
      
      document.getElementById('jobTitle').value = "";
      document.getElementById('phoneNumber').value = "";
      document.getElementById('isPercent').checked = false; // Convert string to boolean
      document.getElementById('pay').value = "";
      document.getElementById('ID').value = "";



  // Change the text of the save button to "Add" or "Save" based on current visibility
  saveButton.name="add";
  saveButton.textContent = (popup.style.display === 'none') ? 'Save' : 'Add';
  togglePayLabelAndValidation();

 
});