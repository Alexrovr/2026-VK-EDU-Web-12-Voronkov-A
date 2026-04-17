const loginForm = document.getElementById('login-form');

if (loginForm) {
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function clearLoginErrors() {
        const emailError = document.getElementById('email-error');
        const passwordError = document.getElementById('password-error');
        const emailField = document.getElementById('email');
        const passwordField = document.getElementById('password');

        [emailError, passwordError].forEach(el => {
            if (el) {
                el.textContent = '';
                el.style.display = 'none';
            }
        });
        [emailField, passwordField].forEach(field => {
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

        const email = document.getElementById('email');
        const password = document.getElementById('password');

        if (!email.value.trim()) {
            showLoginError('email', 'Это поле обязательно для заполнения');
            isValid = false;
        } else if (!isValidEmail(email.value.trim())) {
            showLoginError('email', 'Пожалуйста, введите корректный email адрес');
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
        const field = document.getElementById('answer');
        if (errorEl) {
            errorEl.textContent = '';
            errorEl.style.display = 'none';
        }
        if (field) field.classList.remove('form-control--invalid');
    }

    function showAnswerError(fieldName, message) {
        const errorEl = document.getElementById(`${fieldName}-error`);
        const field = document.getElementById(fieldName);
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.style.display = 'block';
        }
        if (field) field.classList.add('form-control--invalid');
    }

    function validateAnswerForm() {
        clearAnswerErrors();
        let isValid = true;

        const answer = document.getElementById('answer');

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

    const answerField = document.getElementById('answer');
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
