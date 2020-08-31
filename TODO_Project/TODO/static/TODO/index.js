console.log('gefeliceerd!');

const bindCreateItem = () => {
    const createForm = document.getElementById('createForm');
    createForm.addEventListener('change', createForm.submit);
};

const makeItemTitleEditable = () => {
    const labels = document.querySelectorAll('label');
    labels.forEach(label => {
        const updateForm = label.parentElement.parentElement;
        const li = updateForm.parentElement;
        const subbmitUpdateForm = () => updateForm.submit();

        label.addEventListener('dblclick', (eventr) => {
            li.classList.add('editing');

            const input = updateForm.querySelector('[name=title]');
            input.className = 'edit';
            input.value = event.target.innerText;
            input.focus();

            const removeEventlistnersAndInput = () => {
                label.removeEventListener('change', updateForm.submit);
                li.classList.remove('editing');
                updateForm.removeChild(input);
                input.className = 'hidden';    
                input.removeEventListener('change', subbmitUpdateForm);
                input.removeEventListener('blur', removeEventlistnersAndInput);        
            };
            input.addEventListener('change', subbmitUpdateForm);
            input.addEventListener('blur', removeEventlistnersAndInput);
        });

        const completed = updateForm.querySelector('[name=completed]');
        if (completed) completed.addEventListener('change', subbmitUpdateForm);
    });
};




bindCreateItem();
makeItemTitleEditable();
