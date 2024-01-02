  // JavaScript code to handle the modal
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("accountModal");
    const openModalBtn = document.getElementById("openModalBtn");
    const closeModalBtn = document.getElementById("closeModal");
    const closeBtn = document.getElementById("closeme");

    const accountNameInput = document.getElementById("accountName");
    const accountNumberInput = document.getElementById("customerName");
    const accountForm = document.getElementById("accountForm");
    const addnew = document.getElementById("save");
    
    // Function to open the modal
    addnew.addEventListener("click", function () {
          const accid = document.getElementById("accountNumber").value;
          const accountname = document.getElementById("accountName").value;
          console.log(accid)
          make_call('save', accid, accountname)
            modal.style.display = "none";
            // generateAccountNumber(); // Generate an autogenerated account number
        });

    // Function to open the modal
    openModalBtn.addEventListener("click", function () {
        modal.style.display = "block";
        generateAccountNumber(); // Generate an autogenerated account number
    });

    // Function to close the modal
    closeModalBtn.addEventListener("click", function () {
        modal.style.display = "none";
        accountForm.reset();
    });
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
        accountForm.reset();
    });

    function generateAccountNumber() {
    // Make an AJAX request to your Django backend to get the next available account number
    fetch("/get_next_customer_number/") // Replace with your Django endpoint URL
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                accountNumberInput.value = data.account_number;
            }
        })
        .catch(error => {
            console.error("Error fetching account number:", error);
        });
}

    // You can also submit the form data to the Django backend using AJAX or a form submission, depending on your preference.
});

   


function make_call(action, accid, accountname) {
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value; // Get the CSRF token from the form
    
 

    // Serialize the form data
    const formData = new FormData();
    formData.append("action", action); // Append the additional data
    formData.append("account_number", accid); // Append the additional data

    formData.append("accountname", accountname); // Append the additional data


    // Make the AJAX request
    fetch("/action/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            // Handle the response as needed
            toastr.success(data['message'], "Howdy!");
            
            // console.log("Response:", data);
        })
        .catch(error => {
            console.error("Error:", error);
        });

    // After successfully submitting the form, hide the modal
    document.getElementById("confirmationModal").style.display = "none";
    setTimeout(function () {
        window.location.reload();
    }, 5000);
}
function DeleteAction(action, rowId, accountname) {
    
    // Handle the response based on the action
    
       // Populate and display the confirmation modal
    const closebt = document.getElementById("closeModals");
    const nobt = document.getElementById("cancelDeleteBtn");
    const conf = document.getElementById("confirmDeleteBtn");

    document.getElementById("confirmationModal").style.display = "block";

    document.getElementById("accountNumberc").value = rowId;
    document.getElementById("accountNamec").value = accountname;
    closebt.addEventListener("click", function () {
      document.getElementById("confirmationModal").style.display =  "none";
        accountForm.reset();
    });
    nobt.addEventListener("click", function () {
      document.getElementById("confirmationModal").style.display =  "none";
        accountForm.reset();
    });
    conf.addEventListener("click", function () {
      make_call(action, rowId,accountname)
      document.getElementById("confirmationModal").style.display =  "none";
        accountForm.reset();
    });




 


    // You can also submit the form data to the Django backend using AJAX or a form submission, depending on your preference.
};