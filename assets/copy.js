document.addEventListener('DOMContentLoaded', function () {
    document.body.addEventListener('click', function (event) {
        if (event.target.tagName === 'A' && event.target.dataset.copy) {
            event.preventDefault();
            var copyText = event.target.dataset.copy;

            var tempInput = document.createElement('input');
            document.body.appendChild(tempInput);
            tempInput.value = copyText;
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);
            // alert('Skopiowano: ' + copyText);
        }
    });
});