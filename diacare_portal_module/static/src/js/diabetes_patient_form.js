document.addEventListener('DOMContentLoaded', function () {
    const dayButtons = document.querySelectorAll('.day-btn');
    const dayForms = document.querySelectorAll('.day-form');

    dayButtons.forEach(button => {
        button.addEventListener('click', () => {
            const dayIndex = button.getAttribute('data-day');
            console.log(`Day clicked: ${dayIndex}`); // Debugging

            // Hide all forms
            dayForms.forEach(form => {
                form.classList.add('d-none');
            });

            // Show the selected day's form
            const selectedForm = document.querySelector(`#day-form-${dayIndex}`);
            if (selectedForm) {
                selectedForm.classList.remove('d-none');
                console.log(`Form shown: #day-form-${dayIndex}`); // Debugging
            } else {
                console.error(`Form not found for #day-form-${dayIndex}`); // Debugging
            }
        });
    });
});
