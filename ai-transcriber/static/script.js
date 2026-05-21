async function uploadFile() {

    const fileInput = document.getElementById("audioFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file");
        return;
    }

    const formData = new FormData();
    formData.append("audio", file);

    const progressContainer = document.getElementById("progressContainer");
    const progressBar = document.getElementById("progressBar");
    const progressText = document.getElementById("progressText");

    progressContainer.style.display = "block";

    let progress = 0;

    const fakeProgress = setInterval(() => {

        if(progress < 90){
            progress += 10;
            progressBar.style.width = progress + "%";
            progressText.innerText = "Processing " + progress + "%";
        }

    }, 500);

    try {

        const response = await fetch("/transcribe", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        clearInterval(fakeProgress);

        progressBar.style.width = "100%";
        progressText.innerText = "Completed ✅";

        if (data.success) {

            document.getElementById("result").value = data.text;

        } else {

            alert(data.error);
        }

    } catch (error) {

        clearInterval(fakeProgress);

        progressText.innerText = "Failed ❌";

        alert("Something went wrong");
    }
}

document.getElementById("downloadBtn").addEventListener("click", () => {

    const text = document.getElementById("result").value;

    const blob = new Blob([text], {
        type: "text/plain"
    });

    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);

    link.download = "transcript.txt";

    link.click();
});