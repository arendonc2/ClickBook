document.addEventListener("DOMContentLoaded", function () {
    const starGroups = document.querySelectorAll('.stars');

    starGroups.forEach(group => {
        const stars = group.querySelectorAll('.star');
        const form = group.closest('form');
        const ratingInput = form.querySelector('.rating-input');

        stars.forEach((star, index) => {
            const rating = index + 1;

            star.addEventListener('mouseover', () => {
                stars.forEach((s, i) => {
                    s.classList.toggle('hover', i < rating);
                });
            });

            star.addEventListener('mouseout', () => {
                stars.forEach(s => s.classList.remove('hover'));
            });

            star.addEventListener('click', async () => {
                ratingInput.value = rating;

                stars.forEach((s, i) => {
                    s.classList.toggle('selected', i < rating);
                });

                const formData = new FormData(form);

                try {
                    await fetch(form.action, {
                        method: 'POST',
                        body: formData
                    });

                    alert('¡Tu calificación fue registrada exitosamente!');
                } catch (error) {
                    alert('Ocurrió un error al registrar tu calificación.');
                }
            });
        });
    });
});

