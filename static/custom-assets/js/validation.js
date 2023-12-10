// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
    'use strict'

    // Select the form inside the modal with class 'needs-validation'
    const modalForm = document.querySelector('.modal .needs-validation')

    // Check if the form is found before attaching the submit event listener
    if (modalForm) {
        modalForm.addEventListener('submit', event => {
            if (!modalForm.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            modalForm.classList.add('was-validated')
        }, false)
    }
})()