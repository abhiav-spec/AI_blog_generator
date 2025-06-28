function generateBlog() {
    const prompt = document.getElementById("prompt").value;
    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = "<p style='color:yellow;'>Generating blog...</p>";

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(res => res.json())
    .then(data => {
        outputDiv.innerHTML = `
            <img src="${data.image_url}" style="width:100%; max-height:300px; object-fit:cover; border-radius: 8px;" />
            <h2>Generated Blog:</h2>
            <div id="blog-content"><p>${data.blog.replace(/\n/g, "<br>")}</p></div>
        `;
    })
    .catch(() => {
        outputDiv.innerHTML = "<p style='color:red;'>Something went wrong. Please try again later.</p>";
    });
}

function downloadPDF() {
    const blogContentEl = document.getElementById("blog-content");
    if (!blogContentEl || blogContentEl.innerText.trim() === "") {
        alert("Please generate a blog first!");
        return;
    }

    const blogText = blogContentEl.innerText;

    const blob = new Blob([blogText], { type: 'application/pdf' });

    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = "AI_Blog.pdf";
    link.click();
}

function typeText(element, text, speed = 40) {
    let i = 0;
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

document.addEventListener("DOMContentLoaded", () => {
    const typingEl = document.querySelector(".typing-text");
    const message = "Developed by Abhinav Kumar based on real information from original source.";
    typeText(typingEl, message);
});
