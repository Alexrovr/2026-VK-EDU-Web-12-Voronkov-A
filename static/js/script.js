const loginForm = document.getElementById('login-form');

if (loginForm) {
    function clearLoginErrors() {
        const usernameError = document.getElementById('username-error');
        const passwordError = document.getElementById('password-error');
        const usernameField = document.getElementById('username');
        const passwordField = document.getElementById('password');

        [usernameError, passwordError].forEach(el => {
            if (el) {
                el.textContent = '';
                el.style.display = 'none';
            }
        });
        [usernameField, passwordField].forEach(field => {
            if (field) field.classList.remove('form-control--invalid');
        });
    }

    function showLoginError(fieldName, message) {
        const errorEl = document.getElementById(`${fieldName}-error`);
        const field = document.getElementById(fieldName);
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.style.display = 'block';
        }
        if (field) field.classList.add('form-control--invalid');
    }

    function validateLoginForm() {
        clearLoginErrors();
        let isValid = true;

        const username = document.getElementById('username');
        const password = document.getElementById('password');

        if (!username.value.trim()) {
            showLoginError('username', 'Это поле обязательно для заполнения');
            isValid = false;
        }

        if (!password.value) {
            showLoginError('password', 'Это поле обязательно для заполнения');
            isValid = false;
        } else if (password.value.length < 6) {
            showLoginError('password', 'Пароль должен содержать минимум 6 символов');
            isValid = false;
        }

        return isValid;
    }

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateLoginForm()) {
            loginForm.submit();
        }
    });

    ['email', 'password'].forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('focus', function() {
                const errorEl = document.getElementById(`${fieldId}-error`);
                if (errorEl) {
                    errorEl.textContent = '';
                    errorEl.style.display = 'none';
                    field.classList.remove('form-control--invalid');
                }
            });
        }
    });
}

const form = document.getElementById('signup-form');

if (form) {
    const fields = {
        username: document.getElementById('username'),
        email: document.getElementById('email'),
        password: document.getElementById('password'),
        repeat_password: document.getElementById('repeat_password'),
        avatar: document.getElementById('avatar')
    };

    const errorElements = {
        username: document.getElementById('username-error'),
        email: document.getElementById('email-error'),
        password: document.getElementById('password-error'),
        repeat_password: document.getElementById('repeat_password-error'),
        avatar: document.getElementById('avatar-error')
    };

    function clearErrors() {
        Object.values(errorElements).forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });
        Object.values(fields).forEach(field => {
            field.classList.remove('form-control--invalid');
        });
    }

    function showError(fieldName, message) {
        errorElements[fieldName].textContent = message;
        errorElements[fieldName].style.display = 'block';
        fields[fieldName].classList.add('form-control--invalid');
    }

    function validateForm() {
        clearErrors();
        let isValid = true;

        if (!fields.username.value.trim()) {
            showError('username', 'Это поле обязательно для заполнения');
            isValid = false;
        } else if (fields.username.value.trim().length < 3) {
            showError('username', 'Имя пользователя должно содержать минимум 3 символа');
            isValid = false;
        }

        if (!fields.email.value.trim()) {
            showError('email', 'Это поле обязательно для заполнения');
            isValid = false;
        } else if (!isValidEmail(fields.email.value.trim())) {
            showError('email', 'Пожалуйста, введите корректный email адрес');
            isValid = false;
        }

        if (!fields.password.value) {
            showError('password', 'Это поле обязательно для заполнения');
            isValid = false;
        } else if (fields.password.value.length < 6) {
            showError('password', 'Пароль должен содержать минимум 6 символов');
            isValid = false;
        }

        if (!fields.repeat_password.value) {
            showError('repeat_password', 'Это поле обязательно для заполнения');
            isValid = false;
        } else if (fields.password.value !== fields.repeat_password.value) {
            showError('repeat_password', 'Пароли должны совпадать');
            isValid = false;
        }

        if (fields.avatar.files.length > 0) {
            const file = fields.avatar.files[0];
            const maxSize = 2 * 1024 * 1024; // 2 МБ
            const validFormats = ['image/png', 'image/jpeg', 'image/jpg'];

            if (file.size > maxSize) {
                showError('avatar', 'Размер файла не должен превышать 2 МБ');
                isValid = false;
            } else if (!validFormats.includes(file.type)) {
                showError('avatar', 'Допускаются только форматы PNG и JPG');
                isValid = false;
            }
        }

        return isValid;
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateForm()) {
            form.submit();
        }
    });

    Object.entries(fields).forEach(([fieldName, field]) => {
        field.addEventListener('focus', function() {
            if (errorElements[fieldName]) {
                errorElements[fieldName].textContent = '';
                errorElements[fieldName].style.display = 'none';
                field.classList.remove('form-control--invalid');
            }
        });
    });
}

const askForm = document.getElementById('ask-form');

if (askForm) {
    function clearAskErrors() {
        ['title', 'text', 'tags'].forEach(fieldId => {
            const errorEl = document.getElementById(`${fieldId}-error`);
            const field = document.getElementById(fieldId);
            if (errorEl) {
                errorEl.textContent = '';
                errorEl.style.display = 'none';
            }
            if (field) field.classList.remove('form-control--invalid');
        });
    }

    function showAskError(fieldName, message) {
        const errorEl = document.getElementById(`${fieldName}-error`);
        const field = document.getElementById(fieldName);
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.style.display = 'block';
        }
        if (field) field.classList.add('form-control--invalid');
    }

    function validateAskForm() {
        clearAskErrors();
        let isValid = true;

        const title = document.getElementById('title');
        const text = document.getElementById('text');
        const tags = document.getElementById('tags');

        if (!title.value.trim()) {
            showAskError('title', 'Это поле обязательно для заполнения');
            isValid = false;
        } else if (title.value.trim().length < 5) {
            showAskError('title', 'Заголовок должен содержать минимум 5 символов');
            isValid = false;
        } else if (title.value.length > 255) {
            showAskError('title', 'Заголовок не должен превышать 255 символов');
            isValid = false;
        }

        if (!text.value.trim()) {
            showAskError('text', 'Это поле обязательно для заполнения');
            isValid = false;
        } else if (text.value.trim().length < 10) {
            showAskError('text', 'Текст вопроса должен содержать минимум 10 символов');
            isValid = false;
        }

        if (tags.value.trim()) {
            const tagList = tags.value.split(',').map(tag => tag.trim());
            if (tagList.some(tag => tag.length < 2)) {
                showAskError('tags', 'Каждый тег должен содержать минимум 2 символа');
                isValid = false;
            }
        }

        return isValid;
    }

    askForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateAskForm()) {
            askForm.submit();
        }
    });

    ['title', 'text', 'tags'].forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('focus', function() {
                const errorEl = document.getElementById(`${fieldId}-error`);
                if (errorEl) {
                    errorEl.textContent = '';
                    errorEl.style.display = 'none';
                    field.classList.remove('form-control--invalid');
                }
            });
        }
    });
}

const answerForm = document.getElementById('answer-form');

if (answerForm) {
    function clearAnswerErrors() {
        const errorEl = document.getElementById('answer-error');
        const field = document.getElementById('id_text');
        if (errorEl) {
            errorEl.textContent = '';
            errorEl.style.display = 'none';
        }
        if (field) field.classList.remove('form-control--invalid');
    }

    function showAnswerError(fieldName, message) {
        const errorEl = document.getElementById(`${fieldName}-error`);
        const field = document.getElementById('id_text');
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.style.display = 'block';
        }
        if (field) field.classList.add('form-control--invalid');
    }

    function validateAnswerForm() {
        clearAnswerErrors();
        let isValid = true;

        const answer = document.getElementById('id_text');

        if (!answer.value.trim()) {
            showAnswerError('answer', 'Ответ не может быть пустым');
            isValid = false;
        } else if (answer.value.trim().length < 5) {
            showAnswerError('answer', 'Ответ должен содержать минимум 5 символов');
            isValid = false;
        }

        return isValid;
    }

    answerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateAnswerForm()) {
            answerForm.submit();
        }
    });

    const answerField = document.getElementById('id_text');
    if (answerField) {
        answerField.addEventListener('focus', function() {
            const errorEl = document.getElementById('answer-error');
            if (errorEl) {
                errorEl.textContent = '';
                errorEl.style.display = 'none';
                answerField.classList.remove('form-control--invalid');
            }
        });
    }
}

function toggleQuestionEdit() {
    const view = document.getElementById('question-view');
    const edit = document.getElementById('question-edit');
    if (view && edit) {
        view.style.display = view.style.display === 'none' ? 'block' : 'none';
        edit.style.display = edit.style.display === 'none' ? 'block' : 'none';
    }
}

function toggleAnswerEdit(answerId) {
    const view = document.getElementById(`answer-view-${answerId}`);
    const edit = document.getElementById(`answer-edit-${answerId}`);
    if (view && edit) {
        view.style.display = view.style.display === 'none' ? 'block' : 'none';
        edit.style.display = edit.style.display === 'none' ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const editQuestionBtn = document.querySelector('[data-action="edit-question"]');
    if (editQuestionBtn) {
        editQuestionBtn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleQuestionEdit();
        });
    }

    const editAnswerBtns = document.querySelectorAll('[data-action="edit-answer"]');
    editAnswerBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const answerId = this.getAttribute('data-answer-id');
            toggleAnswerEdit(answerId);
        });
    });

    const cancelQuestionBtns = document.querySelectorAll('[data-action="cancel-question-edit"]');
    cancelQuestionBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleQuestionEdit();
        });
    });

    const cancelAnswerBtns = document.querySelectorAll('[data-action="cancel-answer-edit"]');
    cancelAnswerBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const answerId = this.getAttribute('data-answer-id');
            toggleAnswerEdit(answerId);
        });
    });
});

function initLiveErrorCleanup() {
    const forms = ['login-form', 'signup-form', 'answer-form', 'ask-form'];

    forms.forEach(formId => {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('input', function(e) {
                const field = e.target;
                const group = field.closest('.form__group') || field.parentElement;

                if (group) {
                    field.classList.remove('form-control--invalid');

                    const errorMessages = group.querySelectorAll('.form__invalid-feedback');
                    errorMessages.forEach(error => {
                        error.textContent = '';
                        error.style.display = 'none';
                    });
                }
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', initLiveErrorCleanup);


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function sendApiRequest(url, method, data) {
    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data)
    });

    if (response.status === 204) return {};
    return response;
}

document.addEventListener('DOMContentLoaded', function() {

    const answerForm = document.getElementById('answer-form');

    if (answerForm) {
        answerForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const btn = e.submitter;
            const url = btn.dataset.url;
            const textField = document.getElementById('id_text');
            const errorEl = document.getElementById('answer-error');

            errorEl.textContent = '';
            errorEl.style.display = 'none';
            textField.classList.remove('form-control--invalid');

            const val = textField.value.trim();
            if (!val) {
                textField.classList.add('form-control--invalid');
                errorEl.textContent = "Ответ не может быть пустым";
                errorEl.style.display = 'block';
                return;
            }

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ text: val })
                });

                if (response.ok) {
                    window.location.reload();
                } else {
                    const data = await response.json();
                    textField.classList.add('form-control--invalid');
                    errorEl.textContent = data.text || "Ошибка при сохранении";
                    errorEl.style.display = 'block';
                }
            } catch (error) {
                errorEl.textContent = "Ошибка соединения с сервером";
                errorEl.style.display = 'block';
            }
        });
    }

    const editQuestionForm = document.getElementById('edit-question-form');

    if (editQuestionForm) {
        editQuestionForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const btn = e.submitter;

            const titleField = document.getElementById('edit-title');
            const textField = document.getElementById('edit-text');
            const titleError = document.getElementById('title-error');
            const textError = document.getElementById('text-error');

            [titleError, textError].forEach(el => { if(el) { el.textContent = ''; el.style.display = 'none'; }});
            [titleField, textField].forEach(f => f.classList.remove('form-control--invalid'));

            let isValid = true;

            if (titleField.value.trim().length < 5) {
                titleField.classList.add('form-control--invalid');
                titleError.textContent = "Заголовок должен содержать минимум 5 символов";
                titleError.style.display = 'block';
                isValid = false;
            }

            if (textField.value.trim().length < 10) {
                textField.classList.add('form-control--invalid');
                textError.textContent = "Текст вопроса должен содержать минимум 10 символов";
                textError.style.display = 'block';
                isValid = false;
            }

            if (!isValid) return;

            const response = await sendApiRequest(btn.dataset.url, 'PATCH', {
                title: titleField.value,
                text: textField.value
            });

            if (response.ok) {
                window.location.reload();
            } else {
                const data = await response.json();
                alert('Ошибка при сохранении: ' + JSON.stringify(data));
            }
        });
    }

    document.addEventListener('submit', async function(e) {
        if (e.target.classList.contains('edit-answer-form')) {
            e.preventDefault();
            const form = e.target;
            const btn = e.submitter;
            const answerId = btn.dataset.answerId;
            const textArea = form.querySelector('textarea');

            const response = await sendApiRequest(btn.dataset.url, 'PATCH', {
                text: textArea.value
            });

            if (response.ok) {
                window.location.reload();
            } else {
                const errorEl = document.getElementById(`answer-edit-error-${answerId}`);
                errorEl.textContent = 'Ответ не может быть пустым';
                errorEl.style.display = 'block';
            }
        }
    });
});
