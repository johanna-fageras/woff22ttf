const form = document.getElementById('uploadForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      resultDiv.textContent = "Processing...";

      const formData = new FormData();
      const fileInput = document.getElementById('fileInput');

      if (fileInput.files.length === 0) {
        resultDiv.textContent = "Please select a file!";
        return;
      }

      formData.append('file', fileInput.files[0]);

      try {
        const response = await fetch('/convert', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const blob = await response.blob();
          const filename = response.headers.get('Content-Disposition')
            ?.split('filename=')[1]
            ?.replace(/"/g, '') || 'converted.ttf';

          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = filename;
          a.click();
          window.URL.revokeObjectURL(url);

          resultDiv.textContent = "Conversion successful!";
        } else {
          const error = await response.text();
          resultDiv.textContent = `Error: ${error}`;
        }
      } catch (err) {
        resultDiv.textContent = `Unexpected error: ${err.message}`;
      }

      form.reset();
    });